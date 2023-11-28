from django import forms
from iprestrict import ip_utils as ipu
from iprestrict import models

class IPRangeForm(forms.ModelForm):
    class Meta:
        model = models.IPRange
        exclude = ()

    def clean(self):
        cleaned_data = super(IPRangeForm, self).clean()
        first_ip = cleaned_data.get('first_ip')
        if first_ip is None:
            # first_ip is Mandatory, so just let the default validator catch this
            return cleaned_data
        version = ipu.get_version(first_ip)
        last_ip = cleaned_data.get('last_ip')
        if last_ip is None:
            # first_ip is Mandatory, so just let the default validator catch this
            return cleaned_data
        cidr = cleaned_data.get('cidr_prefix_length')
        if cidr is not None:
            if version == ipu.IPv4 and not (1 <= cidr <= 31):
                self.add_error('cidr_prefix_length', 'Must be a number between 1 and 31')
                return cleaned_data
            if version == ipu.IPv6 and not (1 <= cidr <= 127):
                self.add_error('cidr_prefix_length', 'Must be a number between 1 and 127')
                return cleaned_data

        if last_ip and cidr:
            raise forms.ValidationError("Don't specify the Last IP if you specified a CIDR prefix length")
        if last_ip:
            if version != ipu.get_version(last_ip):
                raise forms.ValidationError(
                    "Last IP should be the same type as First IP (%s)" % version)
            if ipu.to_number(first_ip) > ipu.to_number(last_ip):
                raise forms.ValidationError("Last IP should be greater than First IP")

        if cidr:
            # With CIDR the starting address could be different than the one
            # the user specified. Making sure it is set to the first ip in the
            # subnet.
            start, end = ipu.cidr_to_range(first_ip, cidr)
            cleaned_data['first_ip'] = ipu.to_ip(start, version=version)

        return cleaned_data
