import pandas as pd
from interop import summary

def parse_bcl_statistics(bcl_path):
    run_name = bcl_path.strip("/").split("/")[-1]
    ar = summary(bcl_path)
    df = pd.DataFrame(ar)
    df["run_name"] = run_name
    return df


# if __name__ == '__main__':
#     df = parse_bcl_statistics("/data/raw/novaseq_A01742/240912_A01742_0294_BHY2MWDMXY/")
#     print(df)