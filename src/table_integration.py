from bcl_parser import parse_bcl_statistics
from multiqc_parser import parse_multiqc_statistics
import pandas as pd
import yaml
import os

with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)


def update_multiqc(config):
    """Update all multiqc data"""
    sequencers = config["sequencers"]
    multiqc_paths = config['multiqc_paths']
    all_summary = []
    all_lanes = []
    all_samples = []
    if os.path.exists("data/multiqc_summary.csv"):
        df_mq_summary = pd.read_csv('data/multiqc_summary.csv')
        df_mq_lanes = pd.read_csv('data/multiqc_lanes.csv')
        df_mq_samples = pd.read_csv('data/multiqc_samples.csv')
        cached_runs = df_mq_summary["run_name"].to_list()
        for mq_path in multiqc_paths:
            runs = os.listdir(mq_path)
            for run_name in runs:
                # print(run_name)
                if run_name not in cached_runs:
                    seq_id = run_name.split("_")[1]
                    sequencer = [x for x in sequencers if seq_id in x][0]
                    outputs = check_multiqc_in_a_run(sequencer, mq_path, run_name)
                    if outputs is not None:
                        all_summary.append(outputs[0])
                        all_lanes.append(outputs[1])
                        all_samples.append(outputs[2])
        if len(all_summary) > 0:
            df_additional = pd.concat(all_summary)
            df_mq_summary = pd.concat([df_mq_summary, df_additional])
            df_additional = pd.concat(all_lanes)
            df_mq_lanes = pd.concat([df_mq_lanes, df_additional])
            df_additional = pd.concat(all_samples)
            df_mq_samples = pd.concat([df_mq_samples, df_additional])
    else:
        for mq_path in multiqc_paths:
            runs = os.listdir(mq_path)
            for run_name in runs:
                seq_id = run_name.split("_")[1]
                # print([seq_id, sequencers])
                try:
                    sequencer = [x for x in sequencers if seq_id in x][0]
                except:
                    continue
                outputs = check_multiqc_in_a_run(sequencer, mq_path, run_name)
                if outputs is not None:
                    all_summary.append(outputs[0])
                    all_lanes.append(outputs[1])
                    all_samples.append(outputs[2])
        df_mq_summary = pd.concat(all_summary)
        df_mq_lanes = pd.concat(all_lanes)
        df_mq_samples = pd.concat(all_samples)
    df_mq_summary.to_csv("data/multiqc_summary.csv")
    df_mq_lanes.to_csv("data/multiqc_lanes.csv")
    df_mq_samples.to_csv("data/multiqc_samples.csv")
    return df_mq_summary, df_mq_lanes, df_mq_samples


def check_multiqc_in_a_run(sequencer, mq_path, run_name):
    try:
        full_path = os.path.join(mq_path, run_name)
        print("loading "+full_path)
        summarydf, by_lane, by_samples = parse_multiqc_statistics(full_path)
        summarydf["sequencer"] = sequencer
        by_lane["sequencer"] = sequencer
        by_samples["sequencer"] = sequencer
        return [summarydf, by_lane, by_samples]
    except:
        print("Error for "+ full_path)
        return None


def update_bclstats(config):
    """Update all the tables"""
    bcl_paths = config['bcl_paths']
    all_bcl_stats = []
    if os.path.exists("data/bcl_stats.csv"):
        df_all_bcl_stats = pd.read_csv('data/bcl_stats.csv')
        cached_runs = df_all_bcl_stats["run_name"].to_list()
        # print(cached_runs)
        for bcl_path in bcl_paths:
            # print(bcl_path)
            sequencer = bcl_path.strip("/").split("/")[-1]
            runs = os.listdir(bcl_path)
            for run_name in runs:
                # print(run_name)
                if run_name not in cached_runs:
                    bcl_stats = check_bcl_in_a_run(sequencer, bcl_path, run_name)
                    if bcl_stats is not None:
                        all_bcl_stats.append(bcl_stats)
        if len(all_bcl_stats) > 0:
            df_additional_bcl_stats = pd.concat(all_bcl_stats)
            df_all_bcl_stats = pd.concat([df_all_bcl_stats,
                                          df_additional_bcl_stats])
    else:
        
        for bcl_path in bcl_paths:
            sequencer = bcl_path.strip("/").split("/")[-1]
            runs = os.listdir(bcl_path)
            for run_name in runs:
                bcl_stats = check_bcl_in_a_run(sequencer, bcl_path, run_name)
                if bcl_stats is not None:
                    all_bcl_stats.append(bcl_stats)
        df_all_bcl_stats = pd.concat(all_bcl_stats)
    df_all_bcl_stats.to_csv("data/bcl_stats.csv")
    return df_all_bcl_stats

def check_bcl_in_a_run(sequencer, bcl_path, run_name):
    try:
        full_path = os.path.join(bcl_path, run_name)
        print("loading "+full_path)
        bcl_stats = parse_bcl_statistics(full_path)
        bcl_stats["sequencer"] = sequencer
        return bcl_stats
    except:
        print("Error for "+ full_path)

if __name__ == '__main__':
    df = update_multiqc(config)
    print(df)