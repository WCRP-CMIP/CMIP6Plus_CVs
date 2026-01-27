
"""
Script used for bulk adding experiments
"""
# experiment id	activity id	experiment	tier	sub experiment id	parent experiment id	required model components	additional allowed model components	start year	end year	min number of years	parent activity id	description
data = \
"""amip-nudge	CERESMIP	Nudged amip	2	none	no parent	AGCM	AER CHEM	1990	2024	35	no parent	Nudged amip: All forcings (single run, nudged winds) with observed SST/SIC
amip-nat	CERESMIP	Amip with Natural forcings	2	none	no parent	AGCM	AER CHEM	1990	2024	35	no parent	Amip with Natural forcings: Solar + volcanic + orbital with observed SST/SIC. All other boundary conditions set to 1850.
amip-ghg	CERESMIP	AMIP with WMGHG-only	2	none	no parent	AGCM	AER CHEM	1990	2024	35	no parent	AMIP with WMGHG-only: Well-mixed greenhouse-gas-only simulations with observed SST/SIC
amip-aer	CERESMIP	AMIP with Aer-only	2	none	no parent	AGCM	AER CHEM	1990	2024	35	no parent	AMIP with Aer-only: Anthropogenic-aerosol-only simulations with observed SST/SIC
amip-slcf	CERESMIP	AMIP with SLCF-only	2	none	no parent	AGCM	AER CHEM	1990	2024	35	no parent	AMIP with SLCF-only: Anthropogenic changes in short-lived climate forcings (for use with models including interactive composition) with observed SST/SIC
amip-sst	CERESMIP	AMIP with SST/SIC-only	2	none	no parent	AGCM	AER CHEM	1990	2024	35	no parent	AMIP with SST/SIC-only: Observed SST/SIC change only
amip-noghg	CERESMIP	AMIP but no ghgs	2	none	no parent	AGCM	AER CHEM	1990	2024	35	no parent	AMIP but no ghgs: As with amip, but no changes in well-mixed GHGs
amip-noaer	CERESMIP	AMIP but no aerosol changes	2	none	no parent	AGCM	AER CHEM	1990	2024	35	no parent	AMIP but no aerosol changes: As with amip, but no changes in aerosols"""


output = {}
for row in data.split("\n"):
    expt_id, activity_id, experiment, tier, sub_expt, parent_expt, req_model_comp, add_model_comp, start, end, min_years,parent_activity, description= row.split("\t")
    addition = {
        expt_id: {
            "activity_id": activity_id.split(),
            "additional_allowed_model_components": add_model_comp.split(),
            "description": description,
            "end": end,
            "experiment": experiment,
            "experiment_id": expt_id,
            "min_number_yrs_per_sim": int(min_years),
            "parent_activity_id": [parent_activity] if parent_activity == "no parent" else parent_activity.split(),
            "parent_experiment_id": [parent_expt] if parent_expt == "no parent" else parent_expt.split(),
            "required_model_components": req_model_comp.split(),
            "start": start,
            "sub_experiment_id": sub_expt.split(),
            "tier": int(tier),
            }
            }
    output.update(addition)

import json
with open('../CMIP6Plus_experiment_id.json') as fh:
    data = json.load(fh)

data["experiment_id"].update(output)
with open('../CMIP6Plus_experiment_id.json', 'w') as fh:
    json.dump(data, fh,  indent=4, sort_keys=True)
