# Low-Resource NLP Pre-Flight Checklist

Run before committing any training or evaluation budget. Each gate costs
seconds; the failures they catch cost hours to days of metered compute.

## Data preparation
1. **Parsed-sample print.** Decode three samples through the FULL data
   loader (after all formatters) and read them. Verify the text field
   contains text, not IDs or speaker labels.
2. **Codepoint diff.** `python codepoint_diff.py refs.txt hyps.txt`
   (also train vs. test). Resolve every confusable group before any
   metric is computed. Normalize with `normalize_unicode.py`.

## Model adaptation setup
3. **Existing tokens only.** Prefer an existing language token, proxy
   slot, or built-in language code over adding a new vocabulary entry
   to a pretrained multilingual model.
4. **Task-mix audit.** Check the instruction-tuning data manifest
   against the capability list the model must serve; a missing minority
   task means a missing capability.

## Training
5. **Three-sentence decode.** Qualitative decode before committing to a
   long run. Input parroting or token streams = stop now.
6. **Loss-direction watch.** Rising loss during continued training on
   clean in-domain data is a stop signal, not a tuning problem.

## Evaluation and reporting
7. **Control-language eval.** Hold out a language the base model already
   supports; evaluate it after fine-tuning. Catastrophic regression
   means the adaptation damaged the model globally.
8. **Dual raw/normalized scores.** Report both, and archive the
   normalizer with the model. One change at a time; pin and version the
   full environment image.
