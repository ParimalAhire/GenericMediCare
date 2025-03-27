import pandas as pd
from django.core.management.base import BaseCommand
from store.models import Medicine, Category

class Command(BaseCommand):
    help = 'Import medicines from XLSX file'

    def handle(self, *args, **kwargs):
        file_path = r"C:\Users\HP8CG\Downloads\GenericMediCare\Dataset.xlsx"  # Update path

        try:
            df = pd.read_excel(file_path)

            medicines = []
            for _, row in df.iterrows():
                try:
                    # Fetch the category object by name
                    category_obj, created = Category.objects.get_or_create(name=row["category"])

                    # Create the medicine object
                    medicine = Medicine(
                        name=row["name"],
                        generic_name=row["generic_name"],
                        manufacturer=row["manufacturer"],
                        price=row["price"],
                        stock_quantity=row["stock_quantity"],
                        description=row["description"],
                        image_url=row["image_url"],
                        category=category_obj,  # Assign the Category object
                        prescription_required=row["prescription_required"],
                        expiry_date=row["expiry_date"],
                    )
                    medicines.append(medicine)

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"❌ Skipped row due to error: {e}"))

            # Bulk insert medicines
            Medicine.objects.bulk_create(medicines)
            self.stdout.write(self.style.SUCCESS("✅ XLSX Data Imported Successfully!"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error: {e}"))
