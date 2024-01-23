## About

This tool can update 90 Day Progress Sheet for both [beginner](https://docs.google.com/spreadsheets/d/1Kmn5rl-QDVaNNHu4-7FSTC9SMLxHIXLGyrv_dQfC0qc/edit?usp=sharing) and [intermediate](https://docs.google.com/spreadsheets/d/1QvmYpuhhQ2FOysKAy0WFltyQ7xdt12hxzOnQxK7oSlc/edit?usp=sharing) trackers for daily scores.

Run it before checking your progress sheet or after you play.

#### Quickstart Guide

1. Follow the quickstart guide under [Voltaic's Benchmark Updater](https://github.com/VoltaicHQ/Progress-Sheet-Updater) up to step 3.
2. Open up the config file. Change last_played, playlist_type, and id under sheets:
  - last_played: Should be day 1 if the sheet is brand new. Otherwise, make it the last time you played the playlist
  - playlist_type: Choose either **beginner** or **intermediate**
  - id: The text after .../d/"**here**". For example: https://docs.google.com/spreadsheets/d/placeholder/edit#gid=0 -> placeholder

##### Example JSON :
```json
{
    "scenario_data": {
        "last_played": "2024-01-21 00:00:00",
        "playlist_type": "beginner",
        "beginner_scenarios": {
            ...data..
        },
        "intermediate_scenarios": {
            ...data..
        }
    },
    "sheets": {
        "id": "aksldjf9231490-8ldfkjafsd"
    }
}
```
