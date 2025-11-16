meta = {"script": __file__, "seed": RNG_SEED, "args": vars(args)}
with open(os.path.join(args.out_dir,"run_metadata.json"), "w") as fh:
    json.dump(meta, fh, indent=2)
