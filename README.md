# Steem Account Recovery with Beem

### Step 1: Create new keys
* **Who**: The owner of the to-be-recovered account
* **Keys** needed: none

```
python 1_prepare_new_keys.py [to-be-recovered-account]
```

Sample output (no real keys):
```
$ python 1_prepare_new_keys.py stmdev

1.) Store the new master password and keys safely!
+-----------------------------+------------------------------------------------------+
|       New PRIVATE keys      |       DO NOT PUBLISH OR FORWARD, STORE SAFELY!       |
+-----------------------------+------------------------------------------------------+
|           Account           |                        stmdev                        |
| New private master password | P5Jzy3gUnXvfLs112KdP9tMiPaxvTL6QqiijhZ96APwsRGnmnN3L |
|    New private active key   | 5JygJLgFueQoWWD8jjCUgtAHPJZhpvnpPHk63Y4C8hF6oUh35f7  |
|   New private posting key   | 5JcNkf34weeuN39pUFEYtMjmmcx5MJBWZ3eecpAAggVFU3kUgj3  |
|     New private memo key    | 5KC9nyuCjXKufrea3NET77B68vLBqL1qPMisJq7zKjyE51tKBMC  |
+-----------------------------+------------------------------------------------------+

2.) Make sure you stored the new password and keys safely!

3.) Forward the new PUBLIC owner key to your recovery account:
+----------------------+-------------------------------------------------------+
| New PUBLIC owner key |         Forward this to your recovery partner         |
+----------------------+-------------------------------------------------------+
|       Account        |                         stmdev                        |
| New public owner key | STM6ATH8dXQVUMi6rmfTYW66SZQfHGX9uyJ4YZQaJMidgxVYamdTu |
+----------------------+-------------------------------------------------------+
```

Forward the new **PUBLIC** owner key to the recovery partner


### Step 2: Request the account recovery
* **Who**: The owner of the corresponding recovery account
* **Keys needed**: Active key of the recovery account

```
python 2_request_recovery.py --account-to-recover [account_name] --recovery-account [recovery_account_name]
```

Sample output:
```
$ python 2_request_recovery.py --account-to-recover stmdev --recovery-account crokkon
Enter new PUBLIC owner key for @stmdev:
Enter active key, owner key or master password for @crokkon:
SUCCESS: @crokkon requested account recovery for stmdev:
{
  "expiration": "2018-11-11T21:54:05",
  "ref_block_num": 26813,
  "ref_block_prefix": 1816042759,
  "operations": [
    [
      "request_account_recovery",
      {
        "recovery_account": "crokkon",
        "account_to_recover": "stmdev",
        "new_owner_authority": {
          "weight_threshold": 1,
          "account_auths": [],
          "key_auths": [
            [
              "STM5zYQg4roKmZDzFG5B9VjCqfRZjxkPH34x2thLmwjRtiZnKJrop",
              "1"
            ]
          ]
        },
        "extensions": []
      }
    ]
  ],
  "extensions": [],
  "signatures": [
    "207811c3564ac180d6f9efbec99e1e928729411652f4dee7d2239ba91aa4b4fe1f75b27a21689f6e7345b32a1f52892028130979cc7014b8b8bf34ac31ad4783d9"
  ]
}
```


### Step 3: Recover the account
* **Who**: The owner of the to-be-recovered account
* **Keys needed**: The old and the new owner key or master password

```
python 3_recover_account.py [account_name]
```

Sample output:
```
$ python 3_recover_account.py stmdev
Enter the old master password or owner key for @stmdev:
Enter the new master password for @stmdev:
SUCCESS: @stmdev recovered:
{
  "expiration": "2018-11-11T22:10:18",
  "ref_block_num": 27137,
  "ref_block_prefix": 2310789009,
  "operations": [
    [
      "recover_account",
      {
        "account_to_recover": "stmdev",
        "new_owner_authority": {
          "weight_threshold": 1,
          "account_auths": [],
          "key_auths": [
            [
              "STM5zYQg4roKmZDzFG5B9VjCqfRZjxkPH34x2thLmwjRtiZnKJrop",
              "1"
            ]
          ]
        },
        "recent_owner_authority": {
          "weight_threshold": 1,
          "account_auths": [],
          "key_auths": [
            [
              "STM8avqhnUrLRLgY32aUAkXNuSTviHRddYGjHMZzt6KLCeLohnobL",
              "1"
            ]
          ]
        },
        "extensions": []
      }
    ]
  ],
  "extensions": [],
  "signatures": [
    "1f11ce5be3ff73a704efd2fcada79f963f206446a99fb40a5dfef552be4f567c1709b3ae2b5bcffbb0071282b9fc31f38352847c71cb3ecf650c258fab892bf372",
    "1f7f22b03e224d2d8ed4a26382a7e6cce02dda23b27031f39623697359c53c074d6aac8ec5d38bab27d8827b1f798c187be9243d0f7dffefdf0d0a396bd70912fb"
  ]
}
SUCCESS: @stmdev updated:
{
  "expiration": "2018-11-11T22:27:51",
  "ref_block_num": 27489,
  "ref_block_prefix": 3641330818,
  "operations": [
    [
      "account_update",
      {
        "account": "stmdev",
        "active": {
          "weight_threshold": 1,
          "account_auths": [],
          "key_auths": [
            [
              "STM8N2h1oPYNtfBWWiygmw3QQUiB5pCJWsaadkAamnGkNQiXKmPfN",
              "1"
            ]
          ]
        },
        "posting": {
          "weight_threshold": 1,
          "account_auths": [
            [
              "mutingproxy.app",
              "1"
            ],
            [
              "steeditor.app",
              "1"
            ]
          ],
          "key_auths": [
            [
              "STM6ifoi9ZvtT98NVCNgHqv59fkJaXZTW3a9B6SPHs85tsjXWHEFt",
              "1"
            ]
          ]
        },
        "memo_key": "STM5iRVNzibT6pqwQu2iQyRjFJFCbtZdVirpsEW26LAxDckeAhkfi",
        "json_metadata": "{\"profile\": {\"location\": \"<loc>\", \"about\": \"@crokkon's playground\", \"website\": \"https://steemit.com/@crokkon\", \"profile_image\": \"https://steemitimages.com/u/stmdev/avatar\"}}"
      }
    ]
  ],
  "extensions": [],
  "signatures": [
    "207531358a828eaf6489a9c44c3e144b608adb00195f5895dafae5b8989e0733a8304e46c990eb80471bb10de8fc7b50833010a1e34e8bb46d19508820d3fc3838"
  ]
}
```
