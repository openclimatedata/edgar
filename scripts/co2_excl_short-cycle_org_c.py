import pandas as pd

from pathlib import Path
from goodtables import validate
from goodtables.cli import _print_report
from datapackage import Package

package = Package('datapackage.json')
for resource in package.resources:
    if resource.tabular:
        report = validate(resource.source, schema=resource.schema.descriptor)

root = Path(__file__).parents[1]

# CO2 excl short-cycle-org C

co2_excl_xls = "v432_CO2_excl_short-cycle_org_C_1970_2012.xls"

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

# For category 1B2 there are sometimes two variants:
#   1B2 Fugitive emissions from gaseous fuels
#   1B2 Fugitive emissions from oil and gas
#
# Affected countries:
# Antigua and Barbuda, Bahamas, Belize, Bermuda, Barbados, Cayman Islands,
# Dominica, Guadeloupe, Grenada, Saint Kitts and Nevis, Saint Lucia,
# Montserrat, Martinique, Turks and Caicos Islands, Saint Vincent and the
# Grenadines, Virgin Islands_British, Falkland Islands (Malvinas), French
# Guiana, Guyana, Suriname, Spain, France, United Kingdom, Iceland,
# Bulgaria, Croatia, Hungary, Lithuania, Poland, Romania, Slovakia, Turkey,
# Moldova, Republic of, Ukraine, Azerbaijan, Russian Federation, Israel,
# Afghanistan, Bhutan, Macao, Lao People's Democratic Republic, Malaysia,
# Papua New Guinea, Japan, Australia
#
# Confirmed via email from EDGAR team that this should be summed together as
# 1B2 Fugitive emissions from oil and gas

cat_1b2 = co2_excl[co2_excl.Category == "1B2"].groupby(["Code", "Year"]).sum()
cat_1b2 = cat_1b2.reset_index()
cat_1b2["Category"] = "1B2"

co2_excl = co2_excl.drop(co2_excl[co2_excl.Category == "1B2"].index)
co2_excl = co2_excl.append(cat_1b2)

co2_excl = co2_excl[["Code", "Category", "Year", "Emissions"]]
co2_excl = co2_excl.sort_values(["Code", "Category", "Year"])

co2_excl.to_csv(
    root / "data/co2_excl_short-cycle_org_c.csv", index=False)

package = Package(str(root / 'datapackage.json'))
resource = package.get_resource("co2_excl_short-cycle_org_c")
report = validate(resource.source, schema=resource.schema.descriptor)

_print_report(report)

