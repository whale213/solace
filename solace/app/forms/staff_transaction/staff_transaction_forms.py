from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, IntegerField, \
    DecimalField, SelectMultipleField, validators, ValidationError, widgets

# Promo choices is an int value because its easier to query for 1 and 0 to apply discounts
# On the customer side of transaction when displaying products for purchase
promo_choices = [ (1, "Yes"), (0, "No") ]

dropdown_choices = [("brand", "Brand"), ("apparel_type", "Apparel Type"), ("category", "Category")]

source_choices = [ ("Suppliers", "Brand's Suppliers"), ("2nd hand", "Donated / 2nd hand") ]

sizes = [
    ("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("XXL", "XXL")
]

colours = [
    ("Red", "Red"), ("Blue", "Blue"), ("Yellow", "Yellow"), ("Others", "Others"),
    ("Black", "Black"), ("White", "White"), ("Brown", "Brown")
]

product_approval_options = [("Approved", "Yes"), ("Rejected", "No")]

req_approval_options = [("Accepted", "Accepted"), ("Rejected", "Rejected"), ("Not Applicable", "Not Applicable")]

delivery_payment_amts = [ ("0", "$0"), ("5", "$5"), ("10", "$10"), 
    ("15", "$15"), ("Not Applicable", "Not Applicable")
]


class CheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


def check_name(form, field):
    strange_chars = "#@!%*?^><+=~][.<>$"
    for chars in field.data:
        if chars in strange_chars:
            raise ValidationError(f"Strange characters such as '{chars}' are not allowed in product name.", )

# Checkbox requires its own data required validation as validators.DataRequired() enforces all checkboxes to be checked.
def check_checkbox(form, field):
    if len(field.data) < 1:
        raise ValidationError(f"All Fields Are Required! Field: {field.name} was incomplete.")

def checkRange(form, field):
    if field.data < 0:
        raise ValidationError("Commission cannot have a value less than $0!")

# Inventory forms
class ProductForm(Form):
    name = StringField('Product Name *', [validators.Length(min=1, max=50), validators.DataRequired(), check_name])
    brand = SelectField("Product Brand *", [validators.DataRequired()])
    apparel_type = SelectField("Type Of Apparel *", [validators.DataRequired()])
    stock = IntegerField("Product Stock *", [validators.number_range(min=1, max=1000), validators.DataRequired()])
    price = DecimalField("Product Price *", [validators.number_range(min=1.00, max=200.00), validators.DataRequired()])
    discount = RadioField("Promo Code Applicable *", [validators.DataRequired()], choices=promo_choices)
    source = RadioField("Product's Source *", [validators.DataRequired()], choices=source_choices)
    category = SelectField("Category *", [validators.DataRequired()])
    sizes = CheckboxField("Sizes *", [check_checkbox], choices=sizes)
    colours = CheckboxField("Colours *", [check_checkbox], choices=colours)
    description = TextAreaField("Product Description *", [validators.DataRequired()], render_kw={"maxlength": 250, "rows": 4, "cols": 11})

class SearchProductForm(Form):
    search = StringField("", validators=[validators.DataRequired()])

class InputSettingForm(Form):
    selected_input = SelectField("Select Dropdown", [validators.DataRequired()], choices=dropdown_choices)
    new_input = StringField("Input Name", [validators.DataRequired()])

# Donation Forms
class ApprovalForm(Form):
    all_products_approved = RadioField("Are All Donations Approved? *", [validators.DataRequired()] ,choices=product_approval_options)
    remarks = TextAreaField("If Not All Donations Approved, Why? (Remarks)", render_kw={"maxlength": 250, "rows": 4, "cols": 11})
    drp_off_or_donate_req_stat = RadioField("Drop Off / Delivery Request Status *", [validators.DataRequired()], choices=req_approval_options)
    req_stat_reason = SelectField("If Applicable: Why Delivery Request Rejected / NA?")
    delivery_payment = RadioField("Total Amount For Delivery Payment *", [validators.DataRequired()], choices=delivery_payment_amts)
    total_commission = DecimalField("Total Amount Collectible After Grading (Leave Empty If Rejected)", [validators.InputRequired(), checkRange])
