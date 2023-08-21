import smartsheet
import logging

# VARIABLES TO MODIFY:
origin_sheet_id = 00000   # Add real origin sheet id here
destination_sheet_id = 1000 # Add real destination sheet id here


#  Map column name to column id
column_map = {}

# Helper function to find cell in a row
def get_cell_by_column_name(row, column_name):
    column_id = column_map[column_name]
    return row.get_column(column_id)


print("Starting ...")

# Initialize client. Uses the API token in the environment variable "SMARTSHEET_ACCESS_TOKEN"
smartsheet_client = smartsheet.Smartsheet()
# Make sure we don't miss any error
smartsheet_client.errors_as_exceptions(True)

# Log all calls
logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

def get_sheet(id):
    """Makes call to Smartsheet API to get sheet."""

    sheet = smartsheet_client.Sheets.get_sheet(id)
    return sheet


def populate_map(sheet):
    """Builds column map - translates column names to column id"""
    for column in sheet.columns:
        column_map[column.title] = column.id


def copy_sheet_rows(origin_sheet, destination_sheet_id):
    """
    Takes origin_sheet as object, destination_sheet_id as integer.
    Expects origin_sheet to have a column with the title "# copies" corresponding
    to the number of times that row should be copied to another sheet.
    Makes calls to Smartsheet API to copy rows corresponding times.
    Returns None.
    """

    for r in origin_sheet:
        # find number of copies needed
        num_copies = get_cell_by_column_name(r, "# copies").value

        row_ids = []
        # repeat row id number corresponding to how many copies needed
        for i in range(num_copies):
            row_ids.append(r.id)

        # copy row to destination sheet
        smartsheet_client.Sheets.copy_rows(
            origin_sheet.id,
            smartsheet.models.CopyOrMoveRowDirective({
                'row_ids': row_ids,
                'to': smartsheet.models.CopyOrMoveRowDestination({
                'sheet_id': destination_sheet_id
                })
            })
        )

    return None


origin_sheet = get_sheet(origin_sheet_id)
populate_map(origin_sheet)
copy_sheet_rows(origin_sheet, destination_sheet_id)

print("Done")
