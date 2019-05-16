#!/bin/bash

echo -e "\nStart to pull ACS tree put to ACS_TREE_DIR......"
ACS_TREE_DIR="$HOME/work/acs_code"
[ -d "$ACS_TREE_DIR" ] && rm -rf $ACS_TREE_DIR
mkdir -p $ACS_TREE_DIR
cd $ACS_TREE_DIR;
echo -e "\n------To repo init------"
repo init -u ssh://android.intel.com/manifest -b platform/android/main -m acs-main >/dev/null 2>&1
echo -e "\n------To repo sync------"
repo sync -j8 >/dev/null 2>&1
echo -e "\n------To repo start PRC_release_branch------"
repo start PRC_release_branch --all >/dev/null 2>&1
echo -e "\n------Finished to pull ACS tree------"

echo -e "\n------read name - update campaign gen rule&code------"
read name

echo -e "\nStart to pull Campaigns......"
CAMPAIGN_DIR="$HOME/campaigns"
[ -d "$CAMPAIGN_DIR" ] && rm -rf $CAMPAIGN_DIR
mkdir -p $CAMPAIGN_DIR
mkdir -p $CAMPAIGN_DIR/m
mkdir -p $CAMPAIGN_DIR/n
mkdir -p $CAMPAIGN_DIR/o
HPALM_USER="cliu14x"
HPALM_PASSWD="yes@2017"
cd $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/support/plangenerator

# #get_requirements()
#sed -i '705s/get_requirements()/#get_requirements()/' campaigngen_hpalm.py

echo -e "\n1 Start to pull hpalm_M.ini_ready......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_M.ini_ready -d $CAMPAIGN_DIR/m/ >/dev/null 2>&1 && echo -e "\n1 Finished to pull hpalm_M.ini_ready" &

echo -e "\n2 Start to pull hpalm_N.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_N.ini -d $CAMPAIGN_DIR/n/ >/dev/null 2>&1 && echo -e "\n2 Finished to pull hpalm_N.ini" &

echo -e "\n3 Start to pull hpalm_reliability_M_ready.ini......"
python campaigngen_hpalm.py -t reliability --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_reliability_M_ready.ini -d $CAMPAIGN_DIR/m/ >/dev/null 2>&1 && echo -e "\n3 Finished to pull hpalm_reliability_M_ready.ini" &

echo -e "\n4 Start to pull hpalm_BT_Headset_N.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_BT_Headset_N.ini -d $CAMPAIGN_DIR/n/ >/dev/null 2>&1 && echo -e "\n4 Finished to pull hpalm_BT_Headset_N.ini" &

echo -e "\n5 Start to pull hpalm_BT_Headset.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_BT_Headset.ini -d $CAMPAIGN_DIR/m/ >/dev/null 2>&1 && echo -e "\n5 Finished to pull hpalm_BT_Headset.ini" &

echo -e "\n6 Start to pull hpalm_Multi_Device.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_Multi_Device.ini -d $CAMPAIGN_DIR/m/ >/dev/null 2>&1 && echo -e "\n6 Finished to pull hpalm_Multi_Device.ini" &

echo -e "\n7 Start to pull hpalm_Multi_Device_N.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_Multi_Device_N.ini -d $CAMPAIGN_DIR/n/ >/dev/null 2>&1 && echo -e "\n7 Finished to pull hpalm_Multi_Device_N.ini" &

echo -e "\n8 Start to pull hpalm_semi_auto_M.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_semi_auto_M.ini -d $CAMPAIGN_DIR/m/ >/dev/null 2>&1 && echo -e "\n8 Finished to pull hpalm_semi_auto_M.ini" &

echo -e "\n9 Start to pull hpalm_N_MR1.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_N_MR1.ini -d $CAMPAIGN_DIR/MR1_TP/ >/dev/null 2>&1 && echo -e "\n9 Finished to pull hpalm_N_MR1.ini" &

echo -e "\n10 Start to pull hpalm_BT_Headset_N_MR1.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_BT_Headset_N_MR1.ini -d $CAMPAIGN_DIR/MR1_TP/ >/dev/null 2>&1 && echo -e "\n10 Finished to pull hpalm_BT_Headset_N_MR1.ini" &

echo -e "\n11 Start to pull hpalm_Multi_Device_N_MR1.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_Multi_Device_N_MR1.ini -d $CAMPAIGN_DIR/MR1_TP/ >/dev/null 2>&1 && echo -e "\n11 Finished to pull hpalm_Multi_Device_N_MR1.ini" &

echo -e "\n12 Start to pull hpalm_O.ini_ready......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_O.ini_ready -d $CAMPAIGN_DIR/o/ >/dev/null 2>&1 && echo -e "\n12 Finished to pull hpalm_O.ini_ready" &

echo -e "\n13 Start to pull hpalm_O_MR1.ini......"
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_O_MR1.ini -d $CAMPAIGN_DIR/O_MR1_TP/ >/dev/null 2>&1 && echo -e "\n13 Finished to pull hpalm_O_MR1.ini" &

echo -e "\n14 Start to pull hpalm_ebimage_O......"
python campaigngen_hpalm.py -t ebimage --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_ebimage_O.ini -d $CAMPAIGN_DIR/o/ >/dev/null 2>&1 && echo -e "\n14 Finished to pull hpalm_ebimage_O.ini" &

echo -e "\n15 Start to pull hpalm_ebimage_O to O_MR1_TP......"
python campaigngen_hpalm.py -t ebimage --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_ebimage_O.ini -d $CAMPAIGN_DIR/O_MR1_TP/ >/dev/null 2>&1 && echo -e "\n15 Finished to pull hpalm_ebimage_O.ini to O_MR1_TP" &

echo -e "\n16 Start to pull hpalm_ebimage_M.ini......"
python campaigngen_hpalm.py -t ebimage --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_ebimage_M.ini -d $CAMPAIGN_DIR/m/ >/dev/null 2>&1 && echo -e "\n16 Finished to pull hpalm_ebimage_M.ini" &


#for user image tag begin------
echo -e "\n Start to pull hpalm_userimage_M.ini......"
python campaigngen_hpalm.py -t userimage --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_userimage_M.ini -d $CAMPAIGN_DIR/m/ >/dev/null 2>&1 && echo -e "\n Finished to pull hpalm_userimage_M.ini" &

echo -e "\n Start to pull hpalm_userdebugimage_M.ini......"
python campaigngen_hpalm.py -t userdebugimage --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_userdebugimage_M.ini -d $CAMPAIGN_DIR/m/ >/dev/null 2>&1 && echo -e "\n Finished to pull hpalm_userdebugimage_M.ini" &

echo -e "\n Start to pull hpalm_userimage_O.ini......"
python campaigngen_hpalm.py -t userimage --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_userimage_O.ini -d $CAMPAIGN_DIR/o/ >/dev/null 2>&1 && echo -e "\n Finished to pull hpalm_userimage_O.ini" &

echo -e "\n Start to pull hpalm_userdebugimage_O.ini......"
python campaigngen_hpalm.py -t userdebugimage --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_userdebugimage_O.ini -d $CAMPAIGN_DIR/o/ >/dev/null 2>&1 && echo -e "\n Finished to pull hpalm_userdebugimage_O.ini" &

echo -e "\n Start to pull hpalm_userimage_O.ini for omr1......"
python campaigngen_hpalm.py -t userimage --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_userimage_O.ini -d $CAMPAIGN_DIR/O_MR1_TP/ >/dev/null 2>&1 && echo -e "\n Finished to pull hpalm_userimage_O.ini for omr1" &

echo -e "\n Start to pull hpalm_userdebugimage_O.ini for omr1......"
python campaigngen_hpalm.py -t userdebugimage --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile hpalm_userdebugimage_O.ini -d $CAMPAIGN_DIR/O_MR1_TP/ >/dev/null 2>&1 && echo -e "\n Finished to pull hpalm_userdebugimage_O.ini for omr1" &
#for user image tag end------


echo -e "\n Start to pull catlog.ini......"
rm -rf tc_catalog.xml
python campaigngen_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile catlog.ini -k >/dev/null 2>&1 && echo -e "\n Finished to pull catlog.ini" &

#ps -ef |grep python |grep campaign
wait
echo -e "\n-------Finished to pull Campaigns--------"


echo -e "\nStart to pull CSV from HPALM......"
CSV_DIR="/tmp/csv"
[ -d "$CSV_DIR" ] && rm -rf $CSV_DIR
mkdir -p $CSV_DIR
cd $ACS_TREE_DIR/acs_test_suites/OTC/utils/Export_csv_tool/export_from_hpalm/
[ -d CSV ] && rm -rf CSV
python csv_hpalm.py --domain SSG --user $HPALM_USER --password $HPALM_PASSWD --project OTC_Android_Testing --filterfile PRC_csv_hpalm.ini >/dev/null 2>&1
cp CSV/* $ACS_TREE_DIR/acs_test_suites/OTC/utils/ACS_to_TRC/ET/AFT/
mv CSV $CSV_DIR
echo -e "\n------Finished to pull CSV------"


echo -e "\nStart to merge pretest & posttest and Copy to ACS_TREE_DIR......"
cd $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/support/plangenerator
for i in `ls $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/M/MR_0/TP/ |grep pretest`;do cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/M/MR_0/TP/$i $CAMPAIGN_DIR/m/CAMPAIGN;done;cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/M/MR_0/TP/Post_Test.xml $CAMPAIGN_DIR/m/CAMPAIGN/;rm -rf $CAMPAIGN_DIR/m/CAMPAIGN/AfW*;rm -rf $CAMPAIGN_DIR/m/CAMPAIGN/GOTA*;./campaign_merge.sh $CAMPAIGN_DIR/m/CAMPAIGN/;cp $CAMPAIGN_DIR/m/CAMPAIGN/* $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/M/MR_0/TP/;cp -r $CAMPAIGN_DIR/m/TC/* $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/TC/;cd $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/M/MR_0/TP/;for i in `ls EnergyManagement* PowerManagement* ThermalManagement* Sensor* System_Touch*`;do sed -i 's/isIoCardUsed="False/isIoCardUsed="True/' $i;done;

cd $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/support/plangenerator
for i in `ls $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/ |grep pretest`;do cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/$i $CAMPAIGN_DIR/n/CAMPAIGN;done;cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/Post_Test.xml $CAMPAIGN_DIR/n/CAMPAIGN/;rm -rf $CAMPAIGN_DIR/n/CAMPAIGN/AfW*;rm -rf $CAMPAIGN_DIR/n/CAMPAIGN/GOTA*;./campaign_merge.sh $CAMPAIGN_DIR/n/CAMPAIGN/;cp $CAMPAIGN_DIR/n/CAMPAIGN/* $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/;cp -r $CAMPAIGN_DIR/n/TC/* $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/TC/;cd $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/;for i in `ls EnergyManagement* PowerManagement* ThermalManagement*`;do sed -i 's/isIoCardUsed="False/isIoCardUsed="True/' $i;done;

cd $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/support/plangenerator
for i in `ls $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/ |grep pretest`;do cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/$i $CAMPAIGN_DIR/MR1_TP/CAMPAIGN;done;cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/Post_Test.xml $CAMPAIGN_DIR/MR1_TP/CAMPAIGN/;rm -rf $CAMPAIGN_DIR/MR1_TP/CAMPAIGN/AfW*;rm -rf $CAMPAIGN_DIR/MR1_TP/CAMPAIGN/GOTA*;./campaign_merge.sh $CAMPAIGN_DIR/MR1_TP/CAMPAIGN/;cp $CAMPAIGN_DIR/MR1_TP/CAMPAIGN/* $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_1/TP/;cp -r $CAMPAIGN_DIR/MR1_TP/TC/* $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/TC/;cd $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_1/TP/;for i in `ls EnergyManagement* PowerManagement* ThermalManagement*`;do sed -i 's/isIoCardUsed="False/isIoCardUsed="True/' $i;done;

cd $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/support/plangenerator
for i in `ls $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/ |grep pretest`;do cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/$i $CAMPAIGN_DIR/o/CAMPAIGN;done;cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/Post_Test.xml $CAMPAIGN_DIR/o/CAMPAIGN/;rm -rf $CAMPAIGN_DIR/o/CAMPAIGN/AfW*;rm -rf $CAMPAIGN_DIR/o/CAMPAIGN/GOTA*;./campaign_merge.sh $CAMPAIGN_DIR/o/CAMPAIGN/;cp $CAMPAIGN_DIR/o/CAMPAIGN/* $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/O/gorden_peak/TP/;cp -r $CAMPAIGN_DIR/o/TC/* $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/TC/;cd $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/O/gorden_peak/TP/;for i in `ls EnergyManagement* PowerManagement* ThermalManagement* Sensor* System_Touch*`;do sed -i 's/isIoCardUsed="False/isIoCardUsed="True/' $i;done;

cd $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/support/plangenerator
for i in `ls $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/ |grep pretest`;do cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/$i $CAMPAIGN_DIR/O_MR1_TP/CAMPAIGN;done;cp $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/N/MR_0/TP/Post_Test.xml $CAMPAIGN_DIR/O_MR1_TP/CAMPAIGN/;rm -rf $CAMPAIGN_DIR/O_MR1_TP/CAMPAIGN/AfW*;rm -rf $CAMPAIGN_DIR/O_MR1_TP/CAMPAIGN/GOTA*;./campaign_merge.sh $CAMPAIGN_DIR/O_MR1_TP/CAMPAIGN/;cp $CAMPAIGN_DIR/O_MR1_TP/CAMPAIGN/* $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/O/MR1/TP/;cp -r $CAMPAIGN_DIR/O_MR1_TP/TC/* $ACS_TREE_DIR/acs_test_suites/OTC/TC/TP/TC/;cd $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional/O/MR1/TP/;for i in `ls EnergyManagement* PowerManagement* ThermalManagement* Sensor* System_Touch*`;do sed -i 's/isIoCardUsed="False/isIoCardUsed="True/' $i;done;
echo -e "\n------Finished to Merge & Copy------"



echo -e "\n------read address---update frop--and update source----"
read address

echo -e "\n------copy frop SystemFunctional_Frop/O/gorden_peak to SystemFunctional_Frop/O/MR1--------"
cp -ar $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional_Frop/O/gorden_peak/. $ACS_TREE_DIR/acs_test_suites/OTC/CAMPAIGN/SystemFunctional_Frop/O/MR1


echo -e "\n------read age---Start to upload code to ACS Tree----"
read age

echo -e "\nStart to upload code to ACS Tree......"
cd $ACS_TREE_DIR/acs_test_suites/
git add -A
git commit -am "Update PRC Campaigns and CSV for weekly release"
repo upload
echo -e "\n------Finished to upload code------"
echo -e "Please go to below link to do the engineering build:\nhttps://buildbot.tl.intel.com/absp/builders/acs-engineering/"
