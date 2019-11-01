# CLI BlockExplorer for Oscillate.
Does what it says. Allows you to view information for the block specified.

# Current Version: 1.1.13

# Change-Log
1.1.13
Added auto-detection for netowkr going passed swap height, 
Minor formatting changes, 
Added spacing to make the code re-arrangement easier.


1.1.12
Added BTT ANN field, 
Custom Daemon notes, 
Added average hash-per-miner


1.1.11
Removed SpookyPool (No response from server), 
Added pool name configuration field, 
Added Telegram config, 
Added feature to print progress of pool information gathering, 
Now tell the user the reasons of the know network percentage variations.



## Forking
Simply goto the config and make the changes.

If you want more/less pools, the copy the code used in line 254 and after. It should not be difficult if you know what a variable is.
Also make sure if you do add/subtract pools that you add it in the print statements. Now good luck and fork this hoe.