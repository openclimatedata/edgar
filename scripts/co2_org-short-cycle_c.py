import pandas as pd

from pathlib import Path
from goodtables import validate
from goodtables.cli import _print_report
from datapackage import Package

root = Path(__file__).parents[1]

# CO2 excl short-cycle-org C

co2_excl_xls = "v432_CO2_org_short-cycle_C_1970_2012.xls"

co2_excl = pd.read_excel(
    root / "archive" / co2_excl_xls,
    skiprows=7)

co2_excl = co2_excl.drop(["IPCC-Annex", "World Region"], axis=1)
categories = ["IPCC", "IPCC_description"]
description = co2_excl[categories].drop_duplicates(
    ).sort_values("IPCC").set_index("IPCC")

co2_excl = co2_excl.drop(["IPCC_description", "Name"], axis=1)

co2_excl = co2_excl.rename(columns={"ISO_A3": "Code", "IPCC": "Category"})

co2_excl = co2_excl.melt(
    id_vars=["Code", "Category"],
    value_vars=range(1970, 2013),
    var_name="Year",
    value_name="Emissions"
)

co2_excl.to_csv(
    root / "data/co2_org-short-cycle_c.csv", index=False)

package = Package(str(root / 'datapackage.json'))
resource = package.get_resource("co2_org-short-cycle_c")
report = validate(resource.source, schema=resource.schema.descriptor)

_print_report(report)
