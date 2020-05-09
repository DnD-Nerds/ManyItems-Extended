import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo, showerror, showwarning, askyesno

import re
import os
import json

import time

import subprocess

currentVersion = "Alpha v1.7"

subprocess.run("\"download.bat\"")
print("\nDownloaded saves")

if not os.path.exists(os.getcwd() + "\\environment") or not os.path.exists(os.getcwd() + "\\environment\\version.txt"):
    print("\nYikes uh it looks like you deleted the environment stuff... this makes ManyItems angery :(")
    print("The {0}\\environment folder tracks things like the true version to make sure that you're running on the right version.".format(os.getcwd()))
    print("\nPlease git pull and restart the app.")
    time.sleep(15)
    subprocess.run("exit")

with open(os.getcwd() + "\\environment\\version.txt", "r") as versionFile:
    if not versionFile.read() == currentVersion:
        print("\nYou don't seem to be on the current version! Try restarting the app or syncing.")
        time.sleep(15)
        subprocess.run("exit")

main = tk.Tk(className="ManyItems")

def makeNewItem(save=None):
    if not save == None:
        print("<M> -> Attempting to find weapon save file {0}.json\n".format(save))
        if os.path.exists(os.getcwd() + "\\saves\\weapons\\" + save + ".json"):
            print("-----> Successfully found save file.")
            print("-----> Loading in data.\n")
            with open(os.getcwd() + "\\saves\\weapons\\" + save + ".json", "r") as saveFile:
                tempItem = json.load(saveFile)
                saveFile.close()
            if not tempItem["itemVersion"] == currentVersion:
                print("-----> Your save is outdated!")
                print("-----> This likely isn't a huge deal, but some things could be unstable or may produce non-fatal errors.\n")
        else:
            print("-----> Unable to find save file.")
            print("-----> Initiating as new weapon.\n")
            print("<M> -> Making new item...\n")
            tempItem = {}
            save = None
    else:
        print("<M> -> Making new item...\n")
        tempItem = {}

    itemWin = tk.Toplevel(main)
    demoNotice = tk.Message(master=itemWin, text="Only a weapon is currently supported as this is a demo.", bg="pink")
    demoNotice.grid(row=0)

    nameFrame = tk.Frame(itemWin, padx=5, pady=5)
    nameFrame.grid(row=1)
    tk.Label(nameFrame, text="Name").grid(row=0, sticky=tk.W)
    tk.Label(nameFrame, text="Type").grid(row=1, sticky=tk.W)
    tk.Label(nameFrame, text="Rarity").grid(row=2, sticky=tk.W)
    nameField = tk.Entry(nameFrame)
    nameField.grid(row=0, sticky=tk.W, column=1)
    typeField = tk.Entry(nameFrame)
    typeField.grid(row=1, sticky=tk.W, column=1)
    rarityField = tk.Entry(nameFrame)
    rarityField.grid(row=2, sticky=tk.W, column=1)

    def openCustomDamage():
        customDamageWin = tk.Toplevel(itemWin)
        tk.Label(customDamageWin, text="Customize Weapon Damage").grid(row=0)
        CDF_BaseDamageFrame = tk.Frame(customDamageWin, padx=5, pady=5)
        CDF_BaseDamageFrame.grid(row=1)
        CDF_BaseDamageFrame.columnconfigure(0, weight=1)
        CDF_BaseDamageFrame.rowconfigure(0, weight=1)
        tk.Label(CDF_BaseDamageFrame, text="Base Damage Stats").grid(row=0, pady=7)
        tk.Label(CDF_BaseDamageFrame, text="Base Damage").grid(row=1, sticky=tk.W)
        tk.Label(CDF_BaseDamageFrame, text="Primary Damage Type(s)").grid(row=2, sticky=tk.W)
        tk.Label(CDF_BaseDamageFrame, text="Range").grid(row=3, sticky=tk.W)
        CDF_damageField = tk.Entry(CDF_BaseDamageFrame, width=7)
        CDF_damageField.grid(row=1, sticky=tk.W, column=1)
        CDF_damageTypeField = tk.Entry(CDF_BaseDamageFrame, width=15)
        CDF_damageTypeField.grid(row=2, sticky=tk.W, column=1)
        CDF_rangeField = tk.Entry(CDF_BaseDamageFrame, width=7)
        CDF_rangeField.grid(row=3, sticky=tk.W, column=1)
        if "customDamage" in tempItem:
           CDF_damageField.insert(0, tempItem["customDamage"]["base"]["damage"])
           CDF_damageTypeField.insert(0, tempItem["customDamage"]["base"]["damageType"])
           CDF_rangeField.insert(0, tempItem["customDamage"]["base"]["range"])
        else:
            tempItem["customDamage"] = {"base": {"damage": "", "damageType": "", "range": ""}}

        CDF_ModFrame = tk.Frame(customDamageWin, padx=5, pady=5)
        tk.Label(CDF_ModFrame, text="Modifiers").grid(row=0, pady=7)
        def moddmginfo(): showinfo(title="Custom Damage: Base Modifiers", message="Base Modifiers (often referred to as \"mods\") are optional ways to make your weapon do many different things, such as adding randomization to your base damage, and adding strengths and weaknesses to it.\n\nThese can be overidden by attacks [Not yet implemented] or modified on in attacks.")
        tk.Button(CDF_ModFrame, text="?", width=3, command=moddmginfo, bg="lightblue").grid(row=0, column=1, sticky=tk.W)
        
        def baseMod(save=None):
            tempBaseMod = {}
            baseModWin = tk.Toplevel(customDamageWin)
            tk.Label(baseModWin, text="Base Mod").grid(row=0)

            BMIDFrame = tk.Frame(baseModWin, padx=5, pady=5)
            BMIDFrame.grid(row=1)
            tk.Label(BMIDFrame, text="Mod ID").grid(row=0, sticky=tk.W)
            baseModIDField = tk.Entry(BMIDFrame)
            baseModIDField.grid(row=0, column=1, sticky=tk.W)
            def baseModIDInfo(): showinfo(master=miscFrame, title="Item ID", message="Mod IDs are a way of storing the modification to your weapon's base damage.\n\nMod IDs must be unique. They may contain a-z/A-Z/0-9, hyphens, and underscores.\n\nUsing the same Mod ID will overwrite your previous save of the mod. This is great for editing mods!")
            tk.Button(BMIDFrame, text="?", width=3, bg="lightblue", command=baseModIDInfo).grid(row=0, column=2, sticky=tk.W)
            
            randomEnabled = tk.BooleanVar()
            chanceEnabled = tk.BooleanVar()
            modStatsFrame = tk.Frame(baseModWin, padx=5, pady=5)
            modStatsFrame.grid(row=2, sticky=tk.W)
            tk.Label(modStatsFrame, text="Base Mod Stats").grid(row=0)
            tk.Checkbutton(modStatsFrame, variable=randomEnabled, text="Randomization", onvalue=True, offvalue=False).grid(row=1, sticky=tk.W)
            tk.Checkbutton(modStatsFrame, variable=chanceEnabled, text="Activation Chance", onvalue=True, offvalue=False).grid(row=2, sticky=tk.W)
            randomMinField = tk.Entry(modStatsFrame, width=5)
            randomMinField.grid(row=1, column=1, sticky=tk.W)
            randomMaxField = tk.Entry(modStatsFrame, width=5)
            randomMaxField.grid(row=1, column=2, sticky=tk.W)
            chanceField = tk.Entry(modStatsFrame, width=7)
            chanceField.grid(row=2, column=1, sticky=tk.W)
            def BMRandInfo(): showinfo(title="Randomization", message="This has two fields. The first is a minimum, and the second is a maximum. The values may be integers, positive or negative, or 0.\n\nThe randomized number will be applied if the mod is ativated, and it will be placed on top of the base damage.")
            tk.Button(modStatsFrame, text="?", bg="lightblue", width=3, command=BMRandInfo).grid(row=1, column=3, sticky=tk.W)
            def BMChanceInfo(): showinfo(title="Activation Chance", message="An activation chance is an optional means to give your mod a chance of being used every time the Base Attack is used.")
            tk.Button(modStatsFrame, text="?", bg="lightblue", width=3, command=BMChanceInfo).grid(row=2, column=2, sticky=tk.W)
            
            bonusFrame = tk.Frame(baseModWin, padx=5, pady=5)
            bonusFrame.grid(row=3, sticky=tk.W)
            tempBaseMod["bonusAgainst"] = []
            bonusField = tk.Entry(bonusFrame)
            bonusField.grid(row=1, column=1, sticky=tk.W)

            slugFrame = tk.Frame(baseModWin, padx=5, pady=5)
            slugField = tk.Entry(slugFrame)
            slugField.grid(row=1, column=1, sticky=tk.W)

            def finishBaseMod():
                """print("-----> Base Mod {0} creation completed.")
                if randomEnabled == False:
                    print("--------> Got no random mod.")
                else:
                    pass"""
                baseModWin.destroy()
            tk.Button(baseModWin, text="Finish", command=finishBaseMod).grid(row=5)
            def confNoSaveBM():
                if askyesno(title="Confirm", message="Are you sure you want to leave without saving?"):
                    print("-----> Base mod not saved; Base mod creation cancelled.\n")
                    print("-----> Base mod stats completed.\n")
                    baseModWin.destroy()
            tk.Button(baseModWin, text="Quit", command=confNoSaveBM).grid(row=6)

        tk.Button(CDF_ModFrame, text="Add Mod", command=baseMod).grid(row=1, sticky=tk.W)
        tk.Button(CDF_ModFrame, text="Edit Mod").grid(row=2, sticky=tk.W)
        def listBaseModIDs():
            if "customDamage" in tempItem:
                if "baseModIDs" in tempItem["customDamage"]:
                    showinfo(title="Base Mod ID List", message=str(tempItem["customDamage"]["baseModIDs"]))
                else:
                    showinfo(title="Base Mod ID List", message="You haven't made any mods yet. Use the \"Add Mod\" button to make a new mod.")
            else:
                showinfo(title="Base Mod ID List", message="You haven't made any mods yet. Use the \"Add Mod\" button to make a new mod.")
        tk.Button(CDF_ModFrame, text="[]", width=3, command=listBaseModIDs, bg="lightgreen").grid(row=2, column=1, sticky=tk.W)
        CDF_ModFrame.grid(row=2, sticky=tk.W)
        def finishCustomDamage():
            tempItem["customDamage"] = {
                "base": {
                    "damage": CDF_damageField.get(),
                    "damageType": CDF_damageTypeField.get(),
                    "range": CDF_rangeField.get()
                }
            }
            print("-----> Custom damage stats updated.\n")

            customDamageWin.destroy()
        tk.Button(customDamageWin, text="Finish", command=finishCustomDamage).grid(row=3)

    damageTypeFrame = tk.Frame(itemWin, padx=5, pady=5)
    damageTypeFrame.grid(row=2, sticky=tk.W)
    tk.Label(damageTypeFrame, text="Open Attacks/Damage").grid(row=0, sticky=tk.W)
    tk.Button(damageTypeFrame, text="Custom Damage Stats", command=openCustomDamage).grid(row=1, sticky=tk.W)
    def customDmgInfo(): showinfo(master=damageTypeFrame, title="Item ID", message="Custom Damage is the more in-depth, free type of damage/attack formatting. This is the more RPG-esque method.")
    tk.Button(damageTypeFrame, text="?", width=3, command=customDmgInfo, bg="lightblue").grid(row=1, column=1, sticky=tk.W)

    miscFrame = tk.Frame(itemWin, padx=5, pady=5)
    miscFrame.grid(row=3, sticky=tk.W)
    tk.Label(miscFrame, pady=7, text="Misc.").grid(row=0)
    tk.Label(miscFrame, text="Item ID").grid(row=1, sticky=tk.W)
    tk.Label(miscFrame, text="Creator Name").grid(row=2, sticky=tk.W)
    tk.Label(miscFrame, text="Any Extra Notes").grid(row=3, sticky=tk.W)
    def itemIDWarn(): showinfo(master=miscFrame, title="Item ID", message="Item IDs must be unique. They may contain a-z/A-Z/0-9, hyphens, and underscores.\n\nUsing the same Item ID will overwrite your previous save of the item. This is great for editing items!")
    idField = tk.Entry(miscFrame, width=13)
    idField.grid(row=1, column=1, sticky=tk.W)
    tk.Button(miscFrame, text="?", width=3, command=itemIDWarn, bg="lightblue").grid(row=1, column=2, sticky=tk.W)
    authorField = tk.Entry(miscFrame, width=13)
    authorField.grid(row=2, column=1, sticky=tk.W)
    fnotesField = ScrolledText(miscFrame, width=20, height=4)
    fnotesField.grid(row=3, column=1, sticky=tk.W)

    if not save == None:
        nameField.insert(0, tempItem["name"])
        typeField.insert(0, tempItem["type"])
        rarityField.insert(0, tempItem["rarity"])
        authorField.insert(0, tempItem["author"])
        idField.insert(0, tempItem["itemID"])
        fnotesField.insert(1.0, tempItem["finalNotes"])

        print("<M> -> Editing from save {0}!\n".format(save))
    
    def endNewItem():
        tempItem["name"] = nameField.get()
        tempItem["type"] = typeField.get()
        tempItem["rarity"] = rarityField.get()
        
        tempItem["author"] = authorField.get()
        tempItem["itemID"] = idField.get()
        tempItem["finalNotes"] = fnotesField.get("1.0", "end-1c")

        tempItem["itemVersion"] = currentVersion

        passed = True

        for k in tempItem:
            if tempItem[k] == "" or len(tempItem[k]) < 1:
                showinfo(title="Missing Field Data", message="Your weapon is missing data in some fields.\n\nYou can use the \"Quit\" button to exit without saving, or make sure all your fields are filled in before continuing. Your weapon will still be saved without field data, but it isn't preferred that you leave things blank.")
                break
        
        if passed == True:
            validID = re.search(r"^[a-zA-Z0-9_\-]+$", tempItem["itemID"])
            if validID == None:
                showinfo(title="Invalid Item ID", message="You provided an invalid Item ID. IDs may contain upper or lowercase ASCII letters, numerals 0-9, underscores, and hyphens, no spaces.\n\nIf you click \"Finish\" again with an invalid ID, your weapon will not be saved, as the ID will be the save file name.")
                passed = False
                print("-----> Found invalid Item ID.\n")
        
        if passed == True:
            print("<I> -> Got item name \"{0}\".".format(tempItem["name"]))
            print("-----> Got item type \"{0}\".".format(tempItem["type"]))
            print("-----> Got item rarity \"{0}\".\n".format(tempItem["rarity"]))

            print("--------> Got item damage \"{0}\".".format(tempItem["customDamage"]["base"]["damage"]))
            print("--------> Got item damage type \"{0}\".".format(tempItem["customDamage"]["base"]["damageType"]))
            print("--------> Got item range \"{0}\".\n".format(tempItem["customDamage"]["base"]["range"]))

            print("-----> Author: {0}\n".format(tempItem["author"]))
            print("-----> Unique Item ID: {0}\n".format(tempItem["itemID"]))

            tfile = os.getcwd()
            if not os.path.exists(tfile + "\\saves"):
                os.mkdir(path=tfile + "\\saves")
                print("-----> Created saves directory.")
            if not os.path.exists(tfile + "\\saves\\weapons"):
                os.mkdir(path=tfile + "\\saves\\weapons")
                print("-----> Created saves\\weapons directory.")
            if os.path.exists(tfile + "\\saves\\weapons\\" + tempItem["itemID"] + ".json"):
                os.remove(tfile + "\\saves\\weapons\\" + tempItem["itemID"] + ".json")
                print("-----> Removed existing weapon " + tempItem["itemID"] + " to be replaced with new one.")
            with open(tfile + "\\saves\\weapons\\" + tempItem["itemID"] + ".json", "w") as save:
                json.dump(tempItem, save, indent=4)
                save.close()
            print("-----> Saved your weapon successfully under " + tfile + "\\saves\\weapons\\" + tempItem["itemID"] + ".json\n")

            itemWin.destroy()
            print("-----> Item creation completed.\n")
    def confNoSave():
        if askyesno(title="Confirm", message="Are you sure you want to leave without saving?"):
            print("-----> Item not saved; Item creation cancelled.\n")
            print("-----> Item creation completed.\n")
            itemWin.destroy()
    leaveButton = tk.Button(itemWin, text="Finish", command=endNewItem)
    leaveButton.grid(row=4)
    tk.Button(itemWin, text="Quit", command=confNoSave).grid(row=5)

def createWLoadWindow():
    WLoadWindow = tk.Toplevel(main)
    tk.Label(WLoadWindow, text="Weapon Item ID").grid(row=0, sticky=tk.W)
    itemIDField = tk.Entry(WLoadWindow, width=13)
    itemIDField.grid(row=0, column=1, sticky=tk.W)
    def loadWItem():
        makeNewItem(itemIDField.get())
        WLoadWindow.destroy()
    tk.Button(WLoadWindow, text="Load", command=loadWItem).grid(row=1)

tk.Label(main, text="ManyItems - " + currentVersion).grid(row=0, sticky=tk.W)
newItem = tk.Button(main, text="New Weapon", command=makeNewItem)
newItem.grid(row=1, sticky=tk.W)
loadItem = tk.Button(main, text="Load Weapon from Save", command=createWLoadWindow)
loadItem.grid(row=2, sticky=tk.W)

main.mainloop()