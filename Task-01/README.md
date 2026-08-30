# Task-01: Prologue
## Level 1
Alright so this one was pretty easy, by inspecting eat.sh I could find that it was checking if the input is a valid file and if it had the execute permission, the script would output the flag. So by simply using `find . -executable` in the directory, all files and directories were displayed that had the execute permission. In that output only a single file is seen which then passed into eat.sh displays the intended output and flag.

## Level 2
We found the awakening signature from the previous level and it only had to be exported as an environment variable here for the script to check. It then mentions that we should run `diff` on the generated files and that outputs a clue for the next level.

## Level 3
The readme mentions that the code may not appear in the same form again and the first thing that comes to mind is base64.
So by searching for the base64 encoded version of the flag in all files with `grep`, we can find the correct file

## Level 4
The readme mentions to ask for its nature, so by running `file` on it we can see that it is a tar archive and extracting it gives a zip archive which on extracting gives us a file with the second cipher fragment.

## Level 5
There is another branch called alternate timeline which must be the one the readme refers to. Switching to it we see a new folder and a hidden directory inside it which contains a script. By combining the fragments we found earlier and passing it to the script, it gives us the repo for level 6.

## Level 6
For this one we had to resolve git merge conflicts. Two files were affected, each one containing one part of the final password.
It could be merged with `git switch pirate_king_path` and `git merge ancient_history` but conflicts show up which had to resolved manually by editing the conflicted files by just combining the lines that conflict.
From both of the files we get the password as 'TheGrandLineRemembers' and to finally input the password to the script, the merge had to be resolved and commited. And finally inputting the password gives the final flag 'FLAG{The_Grand_Line_Remembers_Your_Commit}'