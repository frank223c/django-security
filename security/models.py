# Copyright (c) 2011, SD Elements. See LICENSE.txt for details.

from datetime import datetime, MINYEAR, MAXYEAR

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

class PasswordExpiry(models.Model):
    """
    Associate a password expiry date with a user. For now, this date is
    effectively just a flag to tell us whether the user has ever changed
    their password, used to force users to change their initial passwords
    when they log in for the first time. Instances are created by
    security.RequirePasswordChangeMiddleware.
    """

    user = models.ForeignKey(User, unique=True) # Not one-to-one because some
                                                # users may never receive an
                                                # expiry date.
    password_expiry_date = models.DateTimeField(default=
                                                 datetime(MINYEAR, 1, 1))

    def is_expired(self):
        return self.password_expiry_date <= datetime.utcnow()

    def never_expire(self):
        self.password_expiry_date = datetime(MAXYEAR, 12, 31)
        self.save()

    class Meta:
        verbose_name_plural = "PasswordExpiries"

# http://www.w3.org/TR/CSP/#sample-violation-report
class CspReport(models.Model):
    """
    Content Security Policy violation report object. Each report represents
    a single alert raised by client browser in response to CSP received from
    the server. Each alert means the browser was unable to access a web resource
    (image, CSS, frame, script) because server's policy prohibited it from accessing
    it. These alerts should be reviewed on regular basis, as they will occur in
    two classes - both requiring attention. First, false positives where too
    restrictive CSP is blocking legitimate website features and needs tuning. Second,
    when real attacks were fired against the user and this raises a question how
    the malicious code appeared on your website. CSP reports are available in
    Django admin view. To be logged into databse, CSP view needs to be configured
    properly.
    """

    # data from CSP report
    document_uri = models.URLField()
    referrer = models.URLField()
    blocked_uri = models.URLField()
    violated_directive = models.CharField(max_length=500)
    original_policy = models.TextField(max_length=500)

    # metadata
    date_received = models.DateTimeField(auto_now_add=True)
    sender_ip = models.GenericIPAddressField()

    def __unicode__(self):
        return 'CSP Report: {0} from {1}'.format(self.blocked_uri, self.document_uri)
