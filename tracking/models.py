from __future__ import unicode_literals, absolute_import
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import format_html
from json2html import json2html

from organisation.models import DepartmentUser, OrgUnit, CostCentre, Location


class CommonFields(models.Model):
    """Fields to be added to all tracking model classes.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    org_unit = models.ForeignKey(
        OrgUnit, on_delete=models.PROTECT, null=True, blank=True)
    cost_centre = models.ForeignKey(
        CostCentre, on_delete=models.PROTECT, null=True, blank=True)
    extra_data = JSONField(null=True, blank=True)

    def extra_data_pretty(self):
        if not self.extra_data:
            return self.extra_data
        try:
            return format_html(json2html.convert(json=self.extra_data))
        except Exception as e:
            return repr(e)

    def save(self, *args, **kwargs):
        if self.cost_centre and not self.org_unit:
            self.org_unit = self.cost_centre.org_position
        elif self.cost_centre and self.cost_centre.org_position and self.org_unit not in self.cost_centre.org_position.get_descendants(include_self=True):
            self.org_unit = self.cost_centre.org_position
        super(CommonFields, self).save(*args, **kwargs)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Computer(CommonFields):
    """Represents a non-mobile computing device. Maps to an object managed by Active Directory.
    """
    sam_account_name = models.CharField(max_length=32, unique=True, null=True)
    hostname = models.CharField(max_length=2048)
    domain_bound = models.BooleanField(default=False)
    ad_guid = models.CharField(max_length=48, null=True, unique=True)
    ad_dn = models.CharField(max_length=512, null=True, unique=True)
    pdq_id = models.IntegerField(null=True, blank=True, unique=True)
    sophos_id = models.CharField(
        max_length=64, unique=True, null=True, blank=True)
    asset_id = models.CharField(
        max_length=64, null=True, blank=True, help_text='OIM Asset ID')
    finance_asset_id = models.CharField(
        max_length=64, null=True, blank=True, help_text='Finance asset ID')
    manufacturer = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    chassis = models.CharField(max_length=128)
    serial_number = models.CharField(max_length=128)
    os_name = models.CharField(max_length=128, blank=True)
    os_version = models.CharField(max_length=128)
    os_service_pack = models.CharField(max_length=128)
    os_arch = models.CharField(max_length=128)
    cpu = models.CharField(max_length=128)
    cpu_count = models.PositiveSmallIntegerField(default=0)
    cpu_cores = models.PositiveSmallIntegerField(default=0)
    memory = models.BigIntegerField(default=0)
    last_ad_login_username = models.CharField(
        max_length=256, null=True, blank=True)
    last_ad_login_date = models.DateField(null=True, blank=True)
    probable_owner = models.ForeignKey(
        DepartmentUser, on_delete=models.PROTECT, blank=True, null=True,
        related_name='computers_probably_owned',
        help_text='Automatically-generated "most probable" device owner.')
    managed_by = models.ForeignKey(
        DepartmentUser, on_delete=models.PROTECT, blank=True, null=True,
        related_name='computers_managed',
        help_text='"Official" device owner/manager (set in AD).')
    date_pdq_updated = models.DateTimeField(null=True, blank=True)
    date_nmap_updated = models.DateTimeField(null=True, blank=True)
    date_sophos_updated = models.DateTimeField(null=True, blank=True)
    date_ad_updated = models.DateTimeField(null=True, blank=True)
    date_dhcp_updated = models.DateTimeField(null=True, blank=True)
    # Notes field to store validation results from synchronising
    # user-uploaded local property register spreadsheets.
    validation_notes = models.TextField(null=True, blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, null=True, blank=True,
        help_text='Physical location')

    def __str__(self):
        return self.hostname


@python_2_unicode_compatible
class Mobile(CommonFields):
    """Represents a mobile computing device. Maps to an object managed by Active Directory.
    """
    ad_guid = models.CharField(max_length=48, null=True, unique=True)
    ad_dn = models.CharField(max_length=512, null=True, unique=True)
    registered_to = models.ForeignKey(
        DepartmentUser, on_delete=models.PROTECT, blank=True, null=True)
    asset_id = models.CharField(
        max_length=64, null=True, help_text='OIM Asset ID')
    finance_asset_id = models.CharField(
        max_length=64, null=True, help_text='Finance asset ID')
    model = models.CharField(max_length=128, null=True)
    os_name = models.CharField(max_length=128, null=True)
    # Identity is a GUID, from Exchange.
    identity = models.CharField(max_length=512, null=True, unique=True)
    serial_number = models.CharField(max_length=128, null=True)
    imei = models.CharField(max_length=64, null=True)
    last_sync = models.DateTimeField(null=True)

    def __str__(self):
        return self.identity


@python_2_unicode_compatible
class EC2Instance(CommonFields):
    """Represents an Amazon EC2 instance.
    """
    name = models.CharField("Instance Name", max_length=200)
    ec2id = models.CharField("EC2 Instance ID", max_length=200, unique=True)
    launch_time = models.DateTimeField(editable=False, null=True, blank=True)
    next_state = models.BooleanField(
        default=True, help_text="Checked is on, unchecked is off")
    running = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'EC2 instance'


@python_2_unicode_compatible
class FreshdeskTicket(models.Model):
    """Cached representation of a Freshdesk ticket, obtained via the
    Freshdesk API.
    """
    # V2 API values below:
    TICKET_SOURCE_CHOICES = (
        (1, 'Email'),
        (2, 'Portal'),
        (3, 'Phone'),
        (7, 'Chat'),
        (8, 'Mobihelp'),
        (9, 'Feedback Widget'),
        (10, 'Outbound Email'),
    )
    TICKET_STATUS_CHOICES = (
        (2, 'Open'),
        (3, 'Pending'),
        (4, 'Resolved'),
        (5, 'Closed'),
    )
    TICKET_PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Urgent'),
    )
    attachments = JSONField(
        null=True, blank=True, default=list,
        help_text='Ticket attachments. An array of objects.')
    cc_emails = JSONField(
        null=True, blank=True, default=list,
        help_text='Email address added in the "cc" field of the incoming ticket email. An array of strings.')
    created_at = models.DateTimeField(null=True, blank=True)
    custom_fields = JSONField(
        null=True, blank=True, default=dict,
        help_text='Key value pairs containing the names and values of custom fields.')
    deleted = models.BooleanField(
        default=False, help_text='Set to true if the ticket has been deleted/trashed.')
    description = models.TextField(
        null=True, blank=True, help_text='HTML content of the ticket.')
    description_text = models.TextField(
        null=True, blank=True, help_text='Content of the ticket in plain text.')
    due_by = models.DateTimeField(
        null=True, blank=True,
        help_text='Timestamp that denotes when the ticket is due to be resolved.')
    email = models.CharField(
        max_length=256, null=True, blank=True, help_text='Email address of the requester.')
    fr_due_by = models.DateTimeField(
        null=True, blank=True,
        help_text='Timestamp that denotes when the first response is due.')
    fr_escalated = models.BooleanField(
        default=False,
        help_text='Set to true if the ticket has been escalated as the result of first response time being breached.')
    fwd_emails = JSONField(
        null=True, blank=True, default=list,
        help_text='Email address(e)s added while forwarding a ticket. An array of strings.')
    group_id = models.BigIntegerField(
        null=True, blank=True,
        help_text='ID of the group to which the ticket has been assigned.')
    is_escalated = models.BooleanField(
        default=False,
        help_text='Set to true if the ticket has been escalated for any reason.')
    name = models.CharField(
        max_length=256, null=True, blank=True, help_text='Name of the requester.')
    phone = models.CharField(
        max_length=256, null=True, blank=True, help_text='Phone number of the requester.')
    priority = models.IntegerField(
        null=True, blank=True, help_text='Priority of the ticket.')
    reply_cc_emails = JSONField(
        null=True, blank=True, default=list,
        help_text='Email address added while replying to a ticket. An array of strings.')
    requester_id = models.BigIntegerField(
        null=True, blank=True, help_text='User ID of the requester.')
    responder_id = models.BigIntegerField(
        null=True, blank=True, help_text='ID of the agent to whom the ticket has been assigned.')
    source = models.IntegerField(
        null=True, blank=True, help_text='The channel through which the ticket was created.')
    spam = models.BooleanField(
        default=False,
        help_text='Set to true if the ticket has been marked as spam.')
    status = models.IntegerField(
        null=True, blank=True, help_text='Status of the ticket.')
    subject = models.TextField(
        null=True, blank=True, help_text='Subject of the ticket.')
    tags = JSONField(
        null=True, blank=True, default=list,
        help_text='Tags that have been associated with the ticket. An array of strings.')
    ticket_id = models.IntegerField(
        unique=True, help_text='Unique ID of the ticket in Freshdesk.')
    to_emails = JSONField(
        null=True, blank=True, default=list,
        help_text='Email addresses to which the ticket was originally sent. An array of strings.')
    type = models.CharField(
        max_length=256, null=True, blank=True, help_text='Ticket type.')
    updated_at = models.DateTimeField(
        null=True, blank=True, help_text='Ticket updated timestamp.')
    # Non-Freshdesk data below.
    freshdesk_requester = models.ForeignKey(
        'FreshdeskContact', on_delete=models.PROTECT, null=True, blank=True,
        related_name='freshdesk_requester')
    freshdesk_responder = models.ForeignKey(
        'FreshdeskContact', on_delete=models.PROTECT, null=True, blank=True,
        related_name='freshdesk_responder')
    du_requester = models.ForeignKey(
        DepartmentUser, on_delete=models.PROTECT, blank=True, null=True,
        related_name='du_requester',
        help_text='Department User who raised the ticket.')
    du_responder = models.ForeignKey(
        DepartmentUser, on_delete=models.PROTECT, blank=True, null=True,
        related_name='du_responder',
        help_text='Department User to whom the ticket is assigned.')
    it_system = models.ForeignKey(
        'registers.ITSystem', blank=True, null=True,
        help_text='IT System to which this ticket relates.')

    def __str__(self):
        return 'Freshdesk ticket ID {}'.format(self.ticket_id)

    def is_support_category(self, category=None):
        """Returns True if ``support_category`` in the ``custom_fields`` dict
        matches the passed-in value, else False.
        """
        if 'support_category' in self.custom_fields and self.custom_fields['support_category'] == category:
            return True
        return False

    def match_it_system(self):
        """Attempt to locate a matching IT System object to associate with.
        First try matching on ``it_system_register_id`` in the custom_fields
        dict, second try matching on category (``Applications``) & subcategory
        (``NAME_OF_APPLICATION``) fields.
        Note that the 2nd match will probably stop working whenever anyone alters
        the support_subcategory field values in Freshdesk.
        """
        from registers.models import ITSystem
        if 'it_system_register_id' in self.custom_fields and self.custom_fields['it_system_register_id']:
            sys_id = self.custom_fields['it_system_register_id']
            if ITSystem.objects.filter(system_id=sys_id).exists():
                self.it_system = ITSystem.objects.get(system_id=sys_id)
                self.save()
        elif self.is_support_category('Applications'):
            if 'support_subcategory' in self.custom_fields and self.custom_fields['support_subcategory']:
                sub = self.custom_fields['support_subcategory']
                # Split on the unicode 'long hyphen':
                if sub.find(u'\u2013') > 0:
                    name = sub.split(u'\u2013')[0].strip()
                    it = ITSystem.objects.filter(name__istartswith=name)
                    if it.count() == 1:  # Matched one IT System by name.
                        self.it_system = it[0]
                        self.save()

    def get_source_display(self):
        """Return the ticket source value description, or None.
        """
        if self.source:
            return next((i[1] for i in self.TICKET_SOURCE_CHOICES if i[0] == self.source), 'Unknown')
        else:
            return None

    def get_status_display(self):
        """Return the ticket status value description, or None.
        """
        if self.status:
            return next((i[1] for i in self.TICKET_STATUS_CHOICES if i[0] == self.status), 'Unknown')
        else:
            return None

    def get_priority_display(self):
        """Return the ticket priority value description, or None.
        """
        if self.priority:
            return next((i[1] for i in self.TICKET_PRIORITY_CHOICES if i[0] == self.priority), 'Unknown')
        else:
            return None


@python_2_unicode_compatible
class FreshdeskConversation(models.Model):
    """Cached representation of a Freshdesk conversation, obtained via the API.
    """
    attachments = JSONField(
        null=True, blank=True, default=list,
        help_text='Ticket attachments. An array of objects.')
    body = models.TextField(
        null=True, blank=True, help_text='HTML content of the conversation.')
    body_text = models.TextField(
        null=True, blank=True, help_text='Content of the conversation in plain text.')
    cc_emails = JSONField(
        null=True, blank=True, default=list,
        help_text='Email address added in the "cc" field of the conversation. An array of strings.')
    created_at = models.DateTimeField(null=True, blank=True)
    conversation_id = models.BigIntegerField(
        unique=True, help_text='Unique ID of the conversation in Freshdesk.')
    from_email = models.CharField(max_length=256, null=True, blank=True)
    incoming = models.BooleanField(
        default=False,
        help_text='Set to true if a particular conversation should appear as being created from outside.')
    private = models.BooleanField(
        default=False,
        help_text='Set to true if the note is private.')
    source = models.IntegerField(
        null=True, blank=True, help_text='Denotes the type of the conversation.')
    ticket_id = models.IntegerField(
        help_text='ID of the ticket to which this conversation is being added.')
    to_emails = JSONField(
        null=True, blank=True, default=list,
        help_text='Email addresses of agents/users who need to be notified about this conversation. An array of strings.')
    updated_at = models.DateTimeField(
        null=True, blank=True, help_text='Ticket updated timestamp.')
    user_id = models.BigIntegerField(
        help_text='ID of the agent/user who is adding the conversation.')
    # Non-Freshdesk data below.
    freshdesk_ticket = models.ForeignKey(
        FreshdeskTicket, on_delete=models.PROTECT, null=True, blank=True)
    freshdesk_contact = models.ForeignKey(
        'FreshdeskContact', on_delete=models.PROTECT, null=True, blank=True)
    du_user = models.ForeignKey(
        DepartmentUser, on_delete=models.PROTECT, blank=True, null=True,
        help_text='Department User who is adding to the conversation.')

    def __str__(self):
        return 'Freshdesk conversation ID {}'.format(self.conversation_id)


@python_2_unicode_compatible
class FreshdeskContact(models.Model):
    """Cached representation of a Freshdesk contact, obtained via the API.
    """
    active = models.BooleanField(
        default=False, help_text='Set to true if the contact has been verified.')
    address = models.CharField(max_length=512, null=True, blank=True)
    contact_id = models.BigIntegerField(
        unique=True, help_text='ID of the contact.')
    created_at = models.DateTimeField(null=True, blank=True)
    custom_fields = JSONField(
        null=True, blank=True, default=dict,
        help_text='Key value pairs containing the names and values of custom fields.')
    description = models.TextField(
        null=True, blank=True, help_text='A short description of the contact.')
    email = models.CharField(
        max_length=256, null=True, blank=True, unique=True,
        help_text='Primary email address of the contact.')
    job_title = models.CharField(
        max_length=256, null=True, blank=True, help_text='Job title of the contact.')
    language = models.CharField(
        max_length=256, null=True, blank=True, help_text='Language of the contact.')
    mobile = models.CharField(
        max_length=256, null=True, blank=True, help_text='Mobile number of the contact.')
    name = models.CharField(
        max_length=256, null=True, blank=True, help_text='Name of the contact.')
    other_emails = JSONField(
        null=True, blank=True, default=list,
        help_text='Additional emails associated with the contact. An array of strings.')
    phone = models.CharField(
        max_length=256, null=True, blank=True, help_text='Phone number of the contact.')
    tags = JSONField(
        null=True, blank=True, default=list,
        help_text='Tags that have been associated with the contact. An array of strings.')
    time_zone = models.CharField(
        max_length=256, null=True, blank=True, help_text='Time zone in which the contact resides.')
    updated_at = models.DateTimeField(
        null=True, blank=True, help_text='Contact updated timestamp.')
    # Non-Freshdesk data below.
    du_user = models.ForeignKey(
        DepartmentUser, on_delete=models.PROTECT, blank=True, null=True,
        help_text='Department User that is represented by this Freshdesk contact.')

    def __str__(self):
        return '{} ({})'.format(self.name, self.email)

    def match_dept_user(self):
        """Attempt to locate a matching DepartmentUser object by email.
        """
        if self.email and DepartmentUser.objects.filter(email__iexact=self.email).exists():
            self.du_user = DepartmentUser.objects.get(email__iexact=self.email)
            self.save()
