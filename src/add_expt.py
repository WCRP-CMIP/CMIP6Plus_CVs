
"""
Script used for bulk adding experiments
"""
# experiment id	activity id	experiment	tier	sub experiment id	parent experiment id	required model components	additional allowed model components	start year	end year	min number of years	parent activity id	description
data = \
"""esm-up2p0-gwl6p0	TIPMIP	zero CO2 emissions simulation starting at global warming level of 6 K, branching off from esm-up2p0	2	none	esm-up2p0	AOGCM BGC	AER CHEM	 	 	300	TIPMIP	stabilisation at GWL6
esm-up2p0-gwl3p0-50y-dn2p0	TIPMIP	ramp down from global warming level of 3K after 50 years, with CO2 emissions that are the negative of those used in esm-up2p0	2	none	esm-up2p0-gwl3p0	AOGCM BGC	AER CHEM	 	 	150	TIPMIP	ramp-down after GWL3
esm-up2p0-gwl1p5-50y-dn2p0	TIPMIP	ramp down from global warming level of 1.5K after 50 years, with CO2 emissions that are the negative of those used in esm-up2p0	2	none	esm-up2p0-gwl1p5	AOGCM BGC	AER CHEM	 	 	75	TIPMIP	ramp-down after GWL1.5
esm-up2p0-gwl3p0-50y-dn2p0-gwl2p0	TIPMIP	zero CO2 emissions simulation branching off from esm-up2p0-gwl3p0-50y-dn2p0 after it passes the 2 K global warming level	2	none	esm-up2p0-gwl3p0-50y-dn2p0	AOGCM BGC	AER CHEM	 	 	300	TIPMIP	stabilisation at GWL2 after temporary overshoot to GWL3
esm-up2p0-gwl3p0-50y-dn2p0-gwl1p5	TIPMIP	zero CO2 emissions simulation branching off from esm-up2p0-gwl3p0-50y-dn2p0 after it passes the 1.5 K global warming level	2	none	esm-up2p0-gwl3p0-50y-dn2p0	AOGCM BGC	AER CHEM	 	 	300	TIPMIP	  stabilisation at GWL1.5 after temporary overshoot to GWL3
esm-up2p0-gwl4p0-50y-dn2p0-gwl0p0	TIPMIP	zero CO2 emissions simulation branching off from esm-up2p0-gwl4p0-50y-dn2p0 after it passes the 0 K global warming level (piControl)	2	none	esm-up2p0-gwl4p0-50y-dn2p0	AOGCM BGC	AER CHEM	 	 	300	TIPMIP	stabilisation at piControl after temporary overshoot to GWL4
esm-up2p0-gwl3p0-50y-dn2p0-gwl0p0	TIPMIP	zero CO2 emissions simulation branching off from esm-up2p0-gwl3p0-50y-dn2p0 after it passes the 0 K global warming level (piControl)	2	none	esm-up2p0-gwl3p0-50y-dn2p0	AOGCM BGC	AER CHEM	 	 	300	TIPMIP	  stabilisation at piControl after temporary overshoot to GWL3
esm-up2p0-gwl2p0-50y-dn2p0-gwl0p0	TIPMIP	zero CO2 emissions simulation branching off from esm-up2p0-gwl2p0-50y-dn2p0 after it passes the 0 K global warming level (piControl)	2	none	esm-up2p0-gwl2p0-50y-dn2p0	AOGCM BGC	AER CHEM	 	 	300	TIPMIP	stabilisation at piControl after temporary overshoot to GWL2
esm-up2p0-gwl4p0-200y-dn2p0	TIPMIP	ramp down from global warming level of 4K after 200 years, with CO2 emissions that are the negative of those used in esm-up2p0	2	none	esm-up2p0-gwl4p0	AOGCM BGC	AER CHEM	 	 	200	TIPMIP	ramp-down after extended period of GWL4
esm-up2p0-gwl3p0-200y-dn2p0	TIPMIP	ramp down from global warming level of 3K after 200 years, with CO2 emissions that are the negative of those used in esm-up2p0	2	none	esm-up2p0-gwl3p0	AOGCM BGC	AER CHEM	 	 	150	TIPMIP	ramp-down after extended period of GWL3
esm-up2p0-gwl2p0-200y-dn2p0	TIPMIP	ramp down from global warming level of 2K after 200 years, with CO2 emissions that are the negative of those used in esm-up2p0	2	none	esm-up2p0-gwl2p0	AOGCM BGC	AER CHEM	 	 	100	TIPMIP	ramp-down after extended period of GWL2
esm-up2p0-gwl4p0-50y-dn1p0	TIPMIP	ramp down from global warming level of 4K after 50 years, with CO2 emissions that are the negative and half the magnitude of those used in esm-up2p0	2	none	esm-up2p0-gwl4p0	AOGCM BGC	AER CHEM	 	 	400	TIPMIP	slow ramp-down after GWL4
esm-up2p0-gwl3p0-50y-dn1p0	TIPMIP	ramp down from global warming level of 3K after 50 years, with CO2 emissions that are the negative and half magnitude of those used in esm-up2p0	2	none	esm-up2p0-gwl3p0	AOGCM BGC	AER CHEM	 	 	300	TIPMIP	slow ramp-down after GWL3
esm-up2p0-gwl2p0-50y-dn1p0	TIPMIP	ramp down from global warming level of 2K after 50 years, with CO2 emissions that are the negative and half the magnitude of those used in esm-up2p0	2	none	esm-up2p0-gwl2p0	AOGCM BGC	AER CHEM	 	 	200	TIPMIP	slow ramp-down after GWL2"""
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
            "parent_activity_id": parent_activity.split(),
            "parent_experiment_id": parent_expt.split(),
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
    json.dump(data, fh,  indent=4)
