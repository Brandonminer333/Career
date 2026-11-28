# Body-worn Camera Traffic Stop Auditor

## Summary

ML pipeline that transcribes and screens body-worn camera footage to help an independent auditor prioritize traffic stops for review under a civil rights settlement. One of three developers; designed the architecture and model stack and built the orchestration, database layer, and classifier suite. Stack: Python, Ray, MySQL, pyannote, faster-whisper, BART-MNLI, Flan-T5, MLflow. Status: prototype, evaluated on an attorney-labeled golden dataset

## Context

In 2022, the ACLU of NorCal, Asian Law Caucus, and Covington & Burling LLP filed *Mathis v. County of Siskiyou*, a civil rights class action alleging discriminatory racial profiling in traffic stops, among other claims ([case page](https://www.aclunorcal.org/press-releases/page/)). On December 29, 2025, the county approved a partial settlement instituting sweeping traffic stop reforms, including retraining all patrol officers on what they can and cannot do during a stop.

Training is only half the battle. The settlement also provides for an impartial auditor who reviews body-worn camera (BWC) footage, but there are roughly 300 stops a month. At about 10 minutes each, reviewing everything takes around 50 hours per month, and reviewer fatigue risks missed violations. The solution is a system that helps point the auditor toward the stops most likely to need a closer look.

## Design constraints

- **Privacy:** The footage is uncensored and contains PII (names, faces, IDs), so processing is restricted to a private GPU server, as required by the governing data terms.
- **No training data or budget:** We had no time or money to hand-transcribe data, so we used pre-trained models and began building an attorney-labeled Golden Dataset for evaluation.
- **Triage, not judgment:** The system never decides compliance. It ranks videos by the number of potential violations flagged, optimizing for **recall over precision**: cast a wide net and let a human catch the false positives.

## Ingestion and storage

Every two months, the county provides a protected link to roughly 24GB of BWC footage (the initial drop was a large historical backlog). Zips are extracted into a datalake-style folder structure. MySQL, already installed on the server, stores metadata (datetime, officer, file path). Videos are referenced by path rather than stored in the database, since each video is read once for audio extraction and afterward only streamed. A lightweight web app lets attorneys and developers stream individual videos without downloading the full footage. Ray orchestrates the pipeline as a DAG of parallel jobs.

## Transcription

Audio is extracted with FFmpeg, then diarized (Pyannote 3.1) and transcribed (Whisper large-v3) in parallel. The outputs are merged into a speaker-attributed, timestamped transcript, and a separate decoder identifies which speaker is the officer. This stage was both the runtime bottleneck and the main accuracy risk: driver audio is much noisier than officer audio, and Whisper can loop on noisy segments, repeating the last phrase.

## Classification

Two zero-shot models handle the audit checks, with no fine-tuning because we lacked labeled data: BART-MNLI classifies transcript content against each settlement requirement, and Flan-T5-large extracts details such as the stated stop reason. Some checks are two-stage (extract the stop reason, then classify it). English proficiency is inferred from proxies: the officer repeating themselves, broken English, and detected non-English words.

## Experiment tracking

We tracked experiments in MLflow. One experiment compared four ways of rendering a transcript for the models (plain text, speaker-prefixed lines, officer-only utterances, and a "storybook" style: `speaker_X said, "..."`), scored against the attorney golden dataset. Officer-only utterances performed best, roughly 10% better than the worst rendering. The gap is small and the golden dataset is small, so I'd treat it as directional and revisit it as the transcription pipeline improves.

## Results

On the Golden Dataset (~120 attorney-labeled videos and counting), adding denoising and diarization improved average accuracy across the measurable requirements by 13.5% relative to a ~50% baseline. Performance varied sharply by check:

- **Stop boundaries:** Detecting the start and end of a stop from greetings and goodbyes was reliable. we could accurately dicern that the officer turned on their bodycam and left it on for the whole duration
- **Stop reason:** Started weak and improved once we classified on all the text rather than the extracted reasone for the stop (A target we care about, but needed improvement).
- **English proficiency:** Stayed poor. It's the most subjective label, it's inferred from a transcript, and driver audio is the noisiest in the footage.

The auditor can use the ranking directly through a web-app login, or ACLU attorneys can review the results and recommend videos to the auditor. If ~80% of ~300 monthly stops are compliant, a reliable ranker could save roughly 40 hours per month (a projection, not a measured result).

## My role

I was one of three developers, building from scratch from November 2025 to a promising prototype by June 2026. I worked 16 hours per week while I was in my Master's program I chose the architecture and models and wrote the database query logic, the Ray DAG, and the classifier suite.

## What I'd do differently

- **Label data sooner.** The biggest bottleneck wasn't modeling, it was trustworthy evaluation data. I'd have prioritized the Golden Dataset from the start and built labeling into the web app itself, so attorneys could watch a video and mark each settlement requirement without leaving the tool.
- **Fine-tune instead of using pre-trained classifiers as-is.** Having no training data was the right constraint for a first prototype, but once the Golden Dataset grows, part of it should become a fine-tuning split.
- **Fix transcription first.** Most downstream weaknesses traced back to Whisper on noisy driver audio, and the team was already looking to replace it.
- **Design the ETL backward from its output.** The county's file structure and formats changed month to month until they finally stabilized, and I spent a lot of time on ingestion code that got refactored. Next time I'd define the output schema first, keep ingestion thin and swappable, and put effort into the stages that don't depend on the county's format.
