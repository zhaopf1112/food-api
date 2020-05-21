# irobot assignment
## requirements
- Reads in ingredients from the command line 
- Use those ingredients to search for recipes online 
- Using the most popular (higher popularity) recipe that contains all of the supplied ingredients, display to the user which ingredients they are missing from the recipe

## How to use 
Our program is written through the Flask framework of Python, and different routing paths are set according to the job requirements, below is the details of how to use it.

### How to deploy
if you deploy the program in linux system(our system is base on Centos7), first you need create the web service with systemd;
#### enter the work directory
```
cd /opt
```
#### pull code into the current server(/opt)
```
git clone https://github.com/zhaopf1112/food-api.git
```
#### set file executable
```
chmod 755 food-api.py
```
#### pip install depended packages
(if you use python2.7, you can use `pip install -r requirements.txt`)
```
pip3 install -r requirements.txt
```

> if your environment is different with my python environment , you need to modify the python directory in the `food-api.py`, also if you want to log the message to the customed directory, you need modify some enviable too.\
> some releted content need to modify is `TOKEN`, and `LOG_DIR`, and python dir in the `food-api.py`.

#### create the systemd service
```
cat /usr/lib/systemd/system/food-api.service

[Unit]
Description=food api server
After=syslog.target network.target

[Service]
WorkingDirectory=/opt/food-api
ExecStart=/opt/food-api/food-api.py

[Install]
WantedBy=multi-user.target
```
#### start and enable the systemd service
```
systemctl start food-api && systemctl enable food-api
```
Now the web service has been started. and the web port is default `5052`, and the host is your os system ip address(you can get the address with the command `hostname -i`,and you need to modify the `yourip` to your os ip address)

### Usage

Reads in ingredients from the command line (you can change the `yourip` with your os specific address), and you can issue this command to get the top 1k ingredients information;
```
curl http://yourip:5052/ingredients
```
and you can get some information output:
```
{
  "data": [
    "acorn squash",
    "adobo sauce",
    "agave nectar",
    "ahi tuna",
    "alfredo pasta sauce",
    "almond extract",
    "almond flour",
    "almond milk"
    ......
  ]
}
```
Use those ingredients to search for recipes online; so we can input the specific ingredients to get the recipes, and you can issue the command below :
```
curl http://yourip:5052/recipes/apples
```
also if you want to put more ingredients to get the related recipes, you can issue the command below:
```
curl http://yourip:5052/recipes/apples,+flour,+sugar
```


and if you want to get the most popular (higher popularity) recipe that contains all of the supplied ingredients, display to the user which ingredients they are missing from the recipe.
you can issue the command below:
```
curl http://yourip:5052/popular_recipes/apples
```
also if you want to put more ingredients to get the most popular recipes, you can issue the command below:
```
curl http://yourip:5052/popular_recipes/apples,+flour,+sugar
```

and the result like below:
```
{
  "data": [
    {
      "id": 591006,
      "image": "https://spoonacular.com/recipeImages/591006-312x231.jpg",
      "imageType": "jpg",
      "likes": 2882,
      "missedIngredientCount": 2,
      "missedIngredients": [
        {
          "aisle": "Nut butters, Jams, and Honey",
          "amount": 1,
          "id": 12195,
          "image": "https://spoonacular.com/cdn/ingredients_100x100/almond-butter.jpg",
          "meta": [],
          "metaInformation": [],
          "name": "almond butter",
          "original": "Almond butter",
          "originalName": "Almond butter",
          "originalString": "Almond butter",
          "unit": "serving",
          "unitLong": "serving",
          "unitShort": "serving"
        },
        {
          "aisle": "Cereal",
          "amount": 1,
          "id": 8212,
          "image": "https://spoonacular.com/cdn/ingredients_100x100/granola.jpg",
          "meta": [],
          "metaInformation": [],
          "name": "granola",
          "original": "Granola",
          "originalName": "Granola",
          "originalString": "Granola",
          "unit": "serving",
          "unitLong": "serving",
          "unitShort": "serving"
        }
      ],
      "title": "Apple Sandwiches with Almond Butter and Granola",
      "unusedIngredients": [],
      "usedIngredientCount": 1,
      "usedIngredients": [
        {
          "aisle": "Produce",
          "amount": 1,
          "id": 9003,
          "image": "https://spoonacular.com/cdn/ingredients_100x100/apple.jpg",
          "meta": [
            "cored",
            "sliced into rings"
          ],
          "metaInformation": [
            "cored",
            "sliced into rings"
          ],
          "name": "apple",
          "original": "1 apple, cored and sliced into rings",
          "originalName": "apple, cored and sliced into rings",
          "originalString": "1 apple, cored and sliced into rings",
          "unit": "",
          "unitLong": "",
          "unitShort": ""
        }
      ]
    }
  ]
}
```
