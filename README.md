# Universal Repository of Flagged IP Addresses
<p align="center">
 <img src="/pics/URFA.png" />
</p>
<table>
<tr>
<td>

*This project's aim is to assist system administrators who are interested in finding out more details about the attackers on their servers and then also be able to do things about it in collaboration with a bunch of other people who are also doing things about it... yeah. This project was created ***by*** cool people ***for*** cool people because it's ***not*** cool when people try to break into your system for no good reason. ***Not*** one iota!*

# Project Concept
*Computer systems experience a ridiculous amount of attacks daily and yet we don't have a universal repository of flagged ip addresses.. until now.*

I hope that this project inspires others to want to participate ,based on the idea that this collected information will help spawn a whole host of applications in the realm of cyber security making the Internet a better safer place with consequences enforced by anyone willing to contribute to weeding these attackers out.
</td>
</tr>
</table>

## Who is this project for ?
>#### Collaborators
>- Linux System admins, who know python.
>- Anyone running Openssh, who knows python.
>- The kid in the back looking for a cool project, who knows python.
>- That seasoned developer ready to take an idea to the next level, who knows python better than all those other guys.
>
>**Collaborator Incentive**
>- Upon contributing you will be given access to an API containing all of the contributed data.
>- The API can be used to build machine learning models.
>- The API can be used in a variety of ways on different projects you can dream up.
>- You will be directly contributing to the safety of the entire Internet.
>
>**Non Collaborators**
>
>This repository is open for anyone to clone so you can still use the updated server logs for your own projects you just wont have access to the API.

-**Disclaimer**

*More then knowing python, so you can read the code and trust it, you need to have super user access to a system preferably **your** system. This project aims at the exact opposite of being malicious so please do not attempt to contribute to this project using someone else's system without their consent and full understanding of it. Keep in mind that none of the contributed material will, and should not, contain any personally specific information pertaining to your server. ie. Your usernames your ip address*

## Instructions
#### Getting Started
<table>
<tr>
<td>

- Install geoip

*Debian Based*
```
$ sudo apt install geoip-bin
```

*Arch Based*
```
$ sudo pacman -S geoip
```

*On RHEL/CentOS/Rocky Linux and friends, there's a small difference. You'll need to install the Extra Packages for Enterprise Linux (EPEL) repository first, then use DNF to install geoiplookup:*
```
$ sudo dnf install geoip
```
- Clone the repository
```
$ git clone
```
- Create a new file to store your failed server logs in

```
$ touch /home/your_user_name/repo_dir/contributors/any_file_name
```
*Now that you have cloned the repo. There are a few ways that you can help the project. I am not a very rigid person so ill just explain the general idea on how to help so you can use your own creative ways to assist. I will say that the format of your data is going to matter and will assist in keeping this project automated so no one has to do work more than once or a couple times really.*

## Data Format

*If your using the lastb command like this:*
```
$ sudo lastb -F
```
*The terminal output should be in this format:*
> anna     ssh:notty    104.238.213.47   Sun Mar 19 13:37:29 2023 - Sun Mar 19 13:37:29 2023  (00:00)
>
>*Note: The -F flag gives us a more precise time format.*

*Send the output of the command to a file*
```
$ sudo lastb -F >> yourfilename (I will refer to this file as the nottys file)
```
*Please save this file inside of the /repo_dir/contributors/yourfilename*

This format is perfect for the setup I've already constructed. If you output this to a file, as is, we can add it to the master repo. If you can manage to contribute this and dont want to do any of the geographic processing no problem I can take care of that part.

*The included scripts in the repo take data in this format and then put it into a pandas dataframe and add two more columns. The data frame after processing ends up looking like the following:*

|User_Name | IP_Addresses  |   Day   |   Month   |  D_of_M  |  Time_UTC  |  Year  |        LATLNG        |    Country   |
| -------- |:-------------:|:-------:|:---------:|:--------:|:----------:|:------:|:--------------------:|:------------:|
| wangyon  | 165.22.62.225 |  Fri    |    Mar    |   10     |  15:19:40  |  2023  | 1.292900, 103.854698 | SG, Singapore|

*Note: Please create or modify the filter in the script as to exclude any of your servers personal information. In fact make sure that no details of your personal server are accidentally included. See the do_many.py script filter section for more info*

**After creating your initial lastb log file keep in mind:**

1. Your server is going to continue accruing more failed logins.
2. Your server was doing this well before you ran the lastb command.

**The idea is now you want to continue to add new entrys to your notty file**

*We want to use as little of our machines processing power so we don't want to keep running the lastb command and getting its entire output we only want to do this once. With this in mind lets walk through how I personally accomplish this:*

```
$ sudo crontab -e
```

***Quick Reference***

| *The crontab format:*

*Min | Hour | Day | Month | Year | COMMAND*

*0 0 30 3 2023 command_to_run_once_march_30_2023_Midnight*

**This is the line in my crontab:**
>01 * * * * lastb -F | head -n 300 >> /home/your_name/repo_dir/contributors/nottys
>
>Keep in mind the number 300 will differ per server depending on the rough estimate of how many attackers are attempting to connect to your system each hour.
>A good idea is to just go through your notty file and quickly estimate how many attacks you are getting hourly and then adjust the head -n number accordingly.

The above cronjob means that in the first minute of every hour the output of the newest 300 entries in the lastb server log are going to be added to the **tail** of the nottys file.

## Overview
At this point you have done enough to contribute and you can stop here. Your next steps are located in the development portion of this readme. You can also choose to run the scripts I created which will greatly help in cleaning and organizing the data. I wont hold you to it and understand either way. 


## (Optional) Running The Provided Scripts

*After modifying the python scripts to work specifically for your server. This means that you updated the folder locations and changed the filters to exclude any unwanted personal server data.*

You can either run the do_once.py file in a terminal
```
$ python do_once.py
```
*Or*

```
$ crontab -e
```

Make a **non sudo** cronjob and then delete
- 05 10 * * * cd /home/your_name/repo_dir/; python do_once.py

*You can check the contents of the progress file which gets created automatically to ensure all finished up fine with no issues.*

```
$ cat progress
```

Running the above command will serve to organize the bulk of the nottys file. You only need to do this once because the next cronjob you set up is going to do this once an hour but for much less entries and it is simply going to add them to the larger original file.

*Keep in mind you already have one sudo cronjob running so you want to give that job a few mins to complete away from your next **non sudo cronjob** *

```
$ crontab -e
```
- 20 * * * * cd /home/your_name/repo_dir/; python do_many.py

</td>
</tr>
</table>


## Use cases
- Cyber Security
- Personal Projects
- Blockchain Technology

### Development
Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

- Fork the repo
- Create a new branch (`git checkout -b improve-feature`)
- Make the appropriate changes in the files
- Add changes to reflect the changes made
- Commit your changes (`git commit -am 'Improve feature'`)
- Push to the branch (`git push origin improve-feature`)
- Create a Pull Request 

### Bug / Feature Request

If you find a bug in this code please let me know.

## Built with 

- [Python](https://www.python.org/) - For its flexibility and abundant amount of resources
- [Numpy](https://numpy.org/) - For computation and updating specific feature data
- [Pandas](https://pandas.pydata.org/) - For organization, processing, data visualization and csv and json file output
- [GeoIP](https://www.maxmind.com/en/geoip-demo) - For obtaining the geographic data on each individual server attacker


## To-do
- Create a CLI UI so collaborators can more easily run an analysis on the data
- Even More
