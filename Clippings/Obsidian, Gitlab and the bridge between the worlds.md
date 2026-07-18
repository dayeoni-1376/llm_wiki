---
title: "Obsidian, Gitlab and the bridge between the worlds"
source: "https://medium.com/@mp.maurer/obsidian-gitlab-and-the-bridge-between-the-worlds-3e937af4940f"
author:
  - "[[Marc Maurer]]"
published: 2026-02-16
created: 2026-07-17
description: "German text below."
tags:
  - "clippings"
---
German text below.

Obsidian is a cool thing. But working with it only on a phone or only on a computer makes it difficult. Keeping data synchronized via complicated workarounds isn’t a practical solution for everyday use. Sure, you can use Obsidian’s own sync function. But I didn’t want to for various reasons. Not least because the “nerd factor” is zero. Dropbox is out too, because sometimes strange things happen with the data there. iCloud is only available in the Apple ecosystem, but since I have to use Windows at work, that’s not an option either. That leaves Git and, for the time being, GitLab or GitHub as a server (I’m planning on having my own server at home).

So, let’s get to work. I cloned the repository on my Mac and then tried the same thing on my iPhone. It didn’t work. I installed WorkingCopy. Still didn’t work. Cloning works, of course, but Obsidian doesn’t register it. Obsidian and WorkingCopy don’t communicate with each other. But was I satisfied with that? No, sir, I haven’t (By the way, this isn’t from AI; it just struck me as funny).

Ultimately, I found a way to make it work despite the iOS hurdles. The principle is simple: The individual apps don’t want to communicate with each other, but they can certainly access each other’s folders. And that’s exactly the way to do it.

To make the instructions easier to follow, here’s my setup:

iOS 18.7.2  
WorkingCopy 6.7.1  
Obsidian 1.11.7

So, except for iOS, these are the latest versions available at the time of writing.

These instructions assume you know how to create a GitLab or GitHub repository and, if desired, clone it to a computer. It also assumes you know how to set up your GitLab/GitHub account in WorkingCopy.

Here’s a step-by-step guide with pictures:

**Obsidian  
**If you haven’t already:

Create a new vault with the same name as your Git repository. It can probably be named differently, but I find this easier.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*hQXqBUzgqWKphqEYgJF3IA.png)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*kMjcYsRs70y-_Kw4XlXGZw.png)

This will create a folder on your iPhone within the Obsidian folder with the vault’s name. Something like this:

On My iPhone/Obsidian/Vault-Name/

After creating the vault, close Obsidian.

**WorkingCopy  
**Tap the + icon in the fingerprint icon in the upper right corner.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*HOtGTZErRV2JaIyAM-pmgg.png)

- Clone repository
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0dAKjT_c-YRKDmqDF-IjFw.png)

- Select the desired repository
- Tap the “chain icon” next to “Working Copy” in “Files app Location”
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*kAvgl_rsjf5lsWck4TMHwA.png)

- The file browser opens
- Go back twice until “On my iPhone” appears at the top
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*3YPCd-RhhSUjpcf7HbSH3w.png)

- Open the Obsidian folder
- Select the folder of the vault you just created and tap “Open” in the upper right corner
- WorkingCopy is now ready to clone the repository into the vault folder → tap “Clone”.

**Back in Obsidian  
**Since the folder into which the repository was cloned contains files and/or folders, the vault is no longer empty. When you start Obsidian now, the content will be indexed.

## Get Marc Maurer’s stories in your inbox

Join Medium for free to get updates from this writer.

Tap the icon in the upper left corner to open the vault’s folder structure.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*JCEHjxYawx8oG4aNYDSPlg.png)

Now you can edit your notes in Obsidian and then synchronize them with Gibbstab via WorkingCopy.

The workflow might look like this:

- Open WorkingCopy
- Pull
- Close WorkingCopy (optional)
- Work in Obsidian
- Open WorkingCopy (if previously closed)
- Commit (the previous step of adding files is no longer necessary, as they are now selected)
- Push

Have fun with Obsidian, Git, and the knowledge that you are now a nerd. Or at least a novice nerd.

Deutscher Text

Obsidian ist eine coole Sache. Aber nur am Handy oder nur am Computer damit arbeiten macht es schwierig. Auch über komplizierte Umwege die Daten synchron zu halten ist im Alltag keine brauchbare Lösung. Gut, man kann natürlich die Obsidian eigene Synch-Funktion in Anspruch zu nehmen. Aber das wollte ich aus verschiedenen Gründen nicht. Nicht zuletzt, weil der Nerd-Faktor hier gleich Null ist. Dropbox geht auch nicht, weil da manchmal mit den Daten komische Sachen passieren. iCloud gibt es nur im Apple Umfeld, aber da ich auf der Arbeit Windows nutzen muss, fällt das auch weg. Was dann noch bleibt ist Git und vorläufig Gitlab oder Github als Server (geplant ist ein eigener Server zu Hause).

Also, frisch ans Werk. Auf dem Mac das Repository geclont und dann auf dem iPhone das gleiche versucht. Geht nicht. WorkingCopy installiert. Geht immer noch nicht. Das Klonen geht natürlich schon, aber Obsidian bekommt davon nichts mit. Obsidian und WorkingCopy sprechen nicht miteinander. Aber habe ich mich damit zufrieden gegeben? Nein, mein Herr, das habe ich nicht (Das stammt übrigens nicht von einer KI, mir kam das nur eben grade witzig vor).

Letztlich fand ich eine Möglichkeit, wie man es trotz der iOS Hürden hinbekommt. Das Prinzip ist einfach erklärt: Die einzelnen Apps wollen zwar nicht miteinander sprechen, aber sie können durchaus auf Ordner der anderen Apps zugreifen. Und genau das ist der Weg.  
Damit die Anleitung nachvollziehbar ist, hier mein Setting:

iOS 18.7.2  
WorkingCopy 6.7.1  
Obsidian 1.11.7

Also bis auf iOS die jeweils aktuellsten verfügbaren Versionen zum Zeitpunkt dieses Artikels.  
Die Anleitung setzt voraus, dass du weisst, wie man ein Gitlab oder -hub Repository anglegt und falls gewünscht, auf einem Computer klont. Auch wird das Wissen vorausgesetzt, wie man in Working Copy seinen Gitlab/-hub Account einrichtet.  
Nun folgt eine Schritt für Schritt Anleitung mit Bildern:

**Obsidian**  
Falls noch nicht geschehen:  
Neuen Vault erstellen mit dem Namen, den das Git Repository hat. Vermutlich kann er auch anders heissen, aber ich finde es so einfacher.  
Das bewirkt, dass auf deinem iPhone im Ordner Obsidian ein Ordner mit dem Namen des Vaults angelegt wird. Also in etwa:  
On My iPhone/Obsidian/Name-des-Vaults/  
Nachdem du den Vault angelegt hast, beende Obsidian.

**WorkingCopy**  
Oben rechts auf das + im Fingerabdruck tippen.  
Clone repository  
Gewünschtes Repository auswählen  
Files app Location auf das «Kettensymbol» tippen  
Filebrowser öffnet sich  
2 x zurück bis oben «auf meinem iPhone» steht  
Den Obsidian Ordner öffnen  
Den Ordner des eben angelegten Vaults auswählen und oben rechts auf öffnen» tippen  
WorkingCopy ist nun bereit das Repository in den Ordner des Vaults zu klonen → auf «clone» tippen.

**Zurück in Obsidian**  
Da der Ordner in den das Repository geklont wurde Dateien und/oder Ordner enthält, ist der Vault nicht mehr leer. Wenn du Obsidian nun startest, wird der Inhalt indexiert.  
Klicke oben links auf das Symbol, das die Ordnerstruktur des Vaults öffnet.  
Jetzt kannst du in Obsidian deine Notizen bearbeiten und sie anschliessend über WorkingCopy mit Gibtlab synchronisieren.  
Der Arbeitsablauf sieht nun so aus:  
WorkingCopy öffnen  
Pull  
WorkingCopy schliessen (optional)  
In Obsidian arbeiten  
WorkingCopy öffnen (falls vorher geschlossen)  
Commit (add als vorheriger Schritt entfällt, weil die Dateien jetzt erst ausgewählt werden)  
Push  
Viel Spass mit Obsidian, Git und dem Wissen, dass du nun ein Nerd bist. Zumindest ein Nerd-Novize.