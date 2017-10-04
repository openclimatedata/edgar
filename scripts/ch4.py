import pandas as pd

from pathlib import Path
from goodtables import validate
from goodtables.cli import _print_report
from datapackage import Package


root = Path(__file__).parents[1]

# CH4

xls_file = "v432_CH4_1970_2012.xls"

df = pd.read_excel(
    root / "archive" / xls_file,
    skiprows=7)

df = df.drop(["IPCC-Annex", "World Region"], axis=1)
categories = ["IPCC", "IPCC_description"]
description = df[categories].drop_duplicates(
    ).sort_values("IPCC").set_index("IPCC")

df = df.drop(["IPCC_description", "Name"], axis=1)

df = df.rename(columns={"ISO_A3": "Code", "IPCC": "Category"})

df = df.melt(
    id_vars=["Code", "Category"],
    value_vars=range(1970, 2013),
    var_name="Year",
    value_name="Emissions"
)

df.to_csv(
    root / "data/ch4.csv", index=False)

package = Package(str(root / 'datapackage.json'))
resource = package.get_resource("ch4")
report = validate(resource.source, schema=resource.schema.descriptor)

_print_report(report)
