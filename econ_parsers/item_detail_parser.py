import json
import urllib

apiKey = ""

if __name__ == "__main__":
  print("Starting...")

  print("Loading JSON")
  with open('items_game.json') as data_file:    
    data = json.load(data_file)

  itemsToParse = []
  with open('treasures.json') as treasures_file:    
    treasures = json.load(treasures_file)

  for treasure in treasures:
    itemsToParse.append(treasure["name"])

    for iDict in treasure["additional_loot"]:
      itemsToParse.append(iDict["name"])

    for iDict in treasure["regular_loot"]:
      itemsToParse.append(iDict["name"])

  #print(treasuresItems)
  #raw_input()

  print("JSON loaded")

  items = data["items_game"]["items"];

  itemsDict = {}
  print("Downloading images URL...")
  j = 0
  for key, item in items.items():
    if j % 50 == 0:
      print(j)
    j += 1
    try:
      if "prefab" in item:
        if item["name"] in itemsToParse:
          if item["prefab"] != "default_item" and "image_inventory" in item:
            print(item["name"])
            
            itemDict={}
            itemDict["name"] = item["name"]
            itemDict["prefab"] = item["prefab"]
            if "item_rarity" in item:
              itemDict["rarity"] = item["item_rarity"]
            else:
              itemDict["rarity"] = "common"

            if "item_quality" in item:
              itemDict["quality"] = item["item_quality"]
            else:
              itemDict["quality"] = "unique"

            if "price_info" in item:
              itemDict["price_info"] = item["price_info"]

            itemDict["image_inventory"] = item["image_inventory"]

            print("\t" + item["image_inventory"])
            url = "https://api.steampowered.com/IEconDOTA2_570/GetItemIconPath/v1/?key=" + apiKey +  "&format=json&iconname=" + item["image_inventory"].split("/")[-1].lower()
            response = urllib.urlopen(url);
            data = json.loads(response.read())
            
            item["image_url"] = ""

            if "result" in data:
              if "path" in data["result"]:
                item["image_url"] = "http://cdn.dota2.com/apps/570/" + data["result"]["path"]
              else:
                item["image_url"] = "NO"
            else:
              item["image_url"] = "NO"
            print("\t" + item["image_url"])

            itemDict["image_url"] = item["image_url"]

            itemsDict[itemDict["name"]] = itemDict

    except Exception as e:
      print("Warning:" + item["name"] + " " +str(e))

  with open('items_detail.json', 'w') as fp:
    json.dump(itemsDict, fp)
