import json
import pandas as pd

def convert_kg_to_lbs(kg, no_decimal=True):
    # set no_decimal = False if want to have decimal values
    if no_decimal:
        return round(kg * 2.2046)
    else:
        return kg * 2.2046


def convert_cm_cube_to_in_cube(cm, no_decimal=True):
    # set no_decimal = False if want to have decimal values
    if no_decimal:
        return round(cm * 0.061024)
    else:
        return cm * 0.061024


def main(in_file, out_file):
    with open(in_file) as f:
        data = f.readlines()
        # create empty pandas dataframe with columns
        my_header = ["order_id", "weight (lbs)", "volume (in3)"]
        df = pd.DataFrame(columns = my_header)

        for d in data:
            # replacing ' with ", so that string is in correct json format
            d = d.replace("'", '"')
            j_data = json.loads(d)
            print ("parsing order number: {}".format(j_data["order_id"]))

            # if data is not in imperial format, convert it
            if j_data["package"]["imperial_unit"] == "false":
                weight = convert_kg_to_lbs(j_data["package"]["weight"])
                volume = convert_cm_cube_to_in_cube(j_data["package"]["volume"])
            else:
                weight = j_data["package"]["weight"]
                volume = j_data["package"]["volume"]

            order_id = j_data["order_id"]

            # append data to the main pandas dataframe
            t = pd.DataFrame([[order_id, weight, volume]], columns =my_header)
            df = df.append(t)
        # convert main data frame to csv file
        # remove index=False, we want index in csv file
        df.to_csv(out_file, index=False)


if __name__ == '__main__':
    in_file = "records.log"
    out_file = 'output.csv'
    main(in_file, out_file)
