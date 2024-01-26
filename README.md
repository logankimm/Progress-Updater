## About

This tool can update 90 Day Progress Sheet for both [beginner](https://docs.google.com/spreadsheets/d/1Kmn5rl-QDVaNNHu4-7FSTC9SMLxHIXLGyrv_dQfC0qc/edit?usp=sharing) and [intermediate](https://docs.google.com/spreadsheets/d/1QvmYpuhhQ2FOysKAy0WFltyQ7xdt12hxzOnQxK7oSlc/edit?usp=sharing) trackers for daily scores.

Run it before checking your progress sheet or after you play.

#### Quickstart Guide

Voltaic has a similar guide [here](https://www.youtube.com/watch?v=awBoG9Jy8CY#t=122) if you would like to use it. The only difference is inputting the correct information to the config file.

1. Download the latest release zip file [here](https://github.com/logankimm/Progress-Updater/releases) and extract it to a preferrable location.
2. Click [here](https://developers.google.com/workspace/guides/create-project) while logged into a google account with permissions to edit your sheet. The following instructions are pretty much on the Voltaic github page [here](https://github.com/VoltaicHQ/Progress-Sheet-Updater) if you would like to use that instead:  
    1. Click the `Go to create a Project` button.
    2. Put any name for `Project Name` field and click the `CREATE`. The Location text does not matter.
    3. Wait until the project has been created(a green notification should appear). Then click `APIs & Services` on the left.
    4. Click the project you just created. You can also select the project name in the top left in the box next to Google Cloud.
    5. The Google Sheets API might be at the bottom of the list - select it if it's there. If not, click  `ENABLE APIS AND SERVICES`. Click `Search for APIs & Services` and type `Google Sheets API`. Click the `Google Sheets API` box. Click `Enable` and wait for it to open.
    6. Click `Credentials`.
    7. Click the `Create Credentials` at the top and select `OAuth client ID`.
    8. Click the `CONFIGURE CONSENT SCREEN` button on the right.
    9. Select the `External` option and click the `CREATE` button underneath it.
    10. In the `App information` section—in the `App name` field, type whatever you want to name your app. In the `User support email` field, type the email address for the Google account that owns your progress sheet. In the `Developer contact information` section near the bottom of the page—in the `Email addresses` field, type the email address for the Google account that owns your progress sheet.
    11. Click the `SAVE AND CONTINUE` button at the bottom of the page.
    12. Click the `ADD OR REMOVE SCOPES` button.
    13. In the `Update selected scopes` menu that opens on the right side of the screen, at the bottom, under the `Manually add scopes` section, paste `www.googleapis.com/auth/spreadsheets` in the text box and click `ADD TO TABLE`.
    14. Click the `UPDATE` button at the bottom of the menu, then click the `SAVE AND CONTINUE` button at the bottom.
    15. Click the `ADD USERS` button, type the email address for the Google account that owns your progress sheet into the text box on the right and click the `ADD` button underneath it.
    16. Click the `SAVE AND CONTINUE` button.
    17. Click `Credentials` on the left menu.
    18. Click the `CREATE CREDENTIALS` button at the top and select `OAuth client ID`.
    19. Click the `Application type` drop-down menu and select `Desktop application`.
    20. In the `Name` field, write whatever name you want and click the `Create` button at the bottom.
    21. Click the `OK` button.
    22. Under the `OAuth 2.0 Client IDs` section, your ID will be listed. Click the download icon on the far right of the row of your newly created ID.
    23. Name it `credentials.json` and save it in the folder with the rest of the program. Capitalization matters so make sure it's all lower case.
3. Open up the config file. Change last_played, playlist_type, and id under sheets:
    - **last_played**: Should be day 1 if the sheet is brand new. Otherwise, make it the last time you played the playlist
    - **playlist_type**: Choose either **beginner** or **intermediate**
    - **id**: The text after .../d/"**here**". For example: https://docs.google.com/spreadsheets/d/placeholder/edit#gid=0 -> placeholder

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
#### Troubleshooting and Notes
- The code assumes that you have done each scenario 3 times as is recommended and will not properly record values otherwise
- If there's any trouble open the debug.log file which should indicate the problem
