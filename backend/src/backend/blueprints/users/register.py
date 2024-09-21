
from . import forms

def create_new_vendor(f: forms.NewVendorSetup) -> List[str]|None:
    """Parse provided form, and return either None or a list of errors raised 
    by the form.
    """
    return []