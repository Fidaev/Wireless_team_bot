import re

import openpyxl  # библиотеки для работы с Ecxel-таблицами
from openpyxl import workbook  #
import os
import sys
import time
import datetime
import string

try:
    os.renames('CFGDATA.xml' or 'CFGDATA.XML', 'CFGDATA.txt')
except:
    print("CFGDATA.xml не найден!")

isxod = "CFGDATA.txt"
otkritie = open(isxod, mode='r')
fayl = otkritie.read()

replacing = fayl
# **********************************************************************************************************************
Vibor = input(""" Если нужно удалить соседей с GUL, то нажмите - 0. 
если нужно удалить соседей с UL, то нажмите - 1. """)

# **********************************************************************************************************************
devip1 = replacing.find("""		<DEVIP>""")
devip2 = replacing.find("""		</DEVIP>""")
devip3 = replacing[devip1:devip2]
devipIP1 = devip3.find("IP")
devipIP2 = devip3.find("</IP>")
devipIP3 = devip3[devipIP1:devipIP2]
oktet = devipIP3.split(".")

start_sctplnk = replacing.find("""	<class>
		<SCTPLNK>""")
finish_sctplnk = replacing.find("""	<class>
		<ACL>""")
old_sctplnk = replacing[start_sctplnk:finish_sctplnk]
new_sctplnk = f"""	<class>
		<SCTPLNK>
			<attributes>
				<SCTPNO>3</SCTPNO>
				<CN>0</CN>
				<SRN>0</SRN>
				<SN>7</SN>
				<MAXSTREAM>17</MAXSTREAM>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<LOCIP>10.80.{oktet[2]}.{oktet[3]}</LOCIP>
				<SECLOCIP>0.0.0.0</SECLOCIP>
				<LOCPORT>1024</LOCPORT>
				<PEERIP>10.6.0.160</PEERIP>
				<SECPEERIP>0.0.0.0</SECPEERIP>
				<PEERPORT>36412</PEERPORT>
				<RTOMIN>1000</RTOMIN>
				<RTOMAX>3000</RTOMAX>
				<RTOINIT>1000</RTOINIT>
				<RTOALPHA>12</RTOALPHA>
				<RTOBETA>25</RTOBETA>
				<HBINTER>5000</HBINTER>
				<MAXASSOCRETR>10</MAXASSOCRETR>
				<MAXPATHRETR>5</MAXPATHRETR>
				<CHKSUMTYPE>1</CHKSUMTYPE><!--CRC32-->
				<AUTOSWITCH>1</AUTOSWITCH><!--Enable-->
				<SWITCHBACKHBNUM>10</SWITCHBACKHBNUM>
				<BLKFLAG>0</BLKFLAG><!--Unblock-->
				<TSACK>200</TSACK>
				<DESCRI></DESCRI>
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
				<VRFIDX>0</VRFIDX>
				<IPVERSION>0</IPVERSION><!--IPv4-->
				<MAXSCTPPDUSIZE>1464</MAXSCTPPDUSIZE>
				<DTLSPOLICYID>255</DTLSPOLICYID><!--NULL-->
			</attributes>
		</SCTPLNK>
		<SCTPLNK>
			<attributes>
				<SCTPNO>2</SCTPNO>
				<CN>0</CN>
				<SRN>0</SRN>
				<SN>7</SN>
				<MAXSTREAM>17</MAXSTREAM>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<LOCIP>10.75.{oktet[2]}.{oktet[3]}</LOCIP>
				<SECLOCIP>0.0.0.0</SECLOCIP>
				<LOCPORT>10002</LOCPORT>
				<PEERIP>10.150.1.149</PEERIP>
				<SECPEERIP>10.150.1.156</SECPEERIP>
				<PEERPORT>58080</PEERPORT>
				<RTOMIN>1000</RTOMIN>
				<RTOMAX>3000</RTOMAX>
				<RTOINIT>1000</RTOINIT>
				<RTOALPHA>12</RTOALPHA>
				<RTOBETA>25</RTOBETA>
				<HBINTER>5000</HBINTER>
				<MAXASSOCRETR>10</MAXASSOCRETR>
				<MAXPATHRETR>5</MAXPATHRETR>
				<CHKSUMTYPE>1</CHKSUMTYPE><!--CRC32-->
				<AUTOSWITCH>1</AUTOSWITCH><!--Enable-->
				<SWITCHBACKHBNUM>10</SWITCHBACKHBNUM>
				<BLKFLAG>0</BLKFLAG><!--Unblock-->
				<TSACK>200</TSACK>
				<DESCRI>Tash_RNC1_0/24/1</DESCRI>
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
				<VRFIDX>0</VRFIDX>
				<IPVERSION>0</IPVERSION><!--IPv4-->
				<MAXSCTPPDUSIZE>1464</MAXSCTPPDUSIZE>
				<DTLSPOLICYID>255</DTLSPOLICYID><!--NULL-->
			</attributes>
		</SCTPLNK>
		<SCTPLNK>
			<attributes>
				<SCTPNO>1</SCTPNO>
				<CN>0</CN>
				<SRN>0</SRN>
				<SN>7</SN>
				<MAXSTREAM>17</MAXSTREAM>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<LOCIP>10.75.{oktet[2]}.{oktet[3]}</LOCIP>
				<SECLOCIP>0.0.0.0</SECLOCIP>
				<LOCPORT>10001</LOCPORT>
				<PEERIP>10.150.1.149</PEERIP>
				<SECPEERIP>10.150.1.156</SECPEERIP>
				<PEERPORT>58080</PEERPORT>
				<RTOMIN>1000</RTOMIN>
				<RTOMAX>3000</RTOMAX>
				<RTOINIT>1000</RTOINIT>
				<RTOALPHA>12</RTOALPHA>
				<RTOBETA>25</RTOBETA>
				<HBINTER>5000</HBINTER>
				<MAXASSOCRETR>10</MAXASSOCRETR>
				<MAXPATHRETR>5</MAXPATHRETR>
				<CHKSUMTYPE>1</CHKSUMTYPE><!--CRC32-->
				<AUTOSWITCH>1</AUTOSWITCH><!--Enable-->
				<SWITCHBACKHBNUM>10</SWITCHBACKHBNUM>
				<BLKFLAG>0</BLKFLAG><!--Unblock-->
				<TSACK>200</TSACK>
				<DESCRI>Tash_RNC1_0/24/1</DESCRI>
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
				<VRFIDX>0</VRFIDX>
				<IPVERSION>0</IPVERSION><!--IPv4-->
				<MAXSCTPPDUSIZE>1464</MAXSCTPPDUSIZE>
				<DTLSPOLICYID>255</DTLSPOLICYID><!--NULL-->
			</attributes>
		</SCTPLNK>
		<SCTPLNK>
			<attributes>
				<SCTPNO>0</SCTPNO>
				<CN>0</CN>
				<SRN>0</SRN>
				<SN>7</SN>
				<MAXSTREAM>17</MAXSTREAM>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<LOCIP>10.70.{oktet[2]}.{oktet[3]}</LOCIP>
				<SECLOCIP>0.0.0.0</SECLOCIP>
				<LOCPORT>2001</LOCPORT>
				<PEERIP>10.150.0.28</PEERIP>
				<SECPEERIP>0.0.0.0</SECPEERIP>
				<PEERPORT>58080</PEERPORT>
				<RTOMIN>1000</RTOMIN>
				<RTOMAX>3000</RTOMAX>
				<RTOINIT>1000</RTOINIT>
				<RTOALPHA>12</RTOALPHA>
				<RTOBETA>25</RTOBETA>
				<HBINTER>5000</HBINTER>
				<MAXASSOCRETR>10</MAXASSOCRETR>
				<MAXPATHRETR>5</MAXPATHRETR>
				<CHKSUMTYPE>1</CHKSUMTYPE><!--CRC32-->
				<AUTOSWITCH>1</AUTOSWITCH><!--Enable-->
				<SWITCHBACKHBNUM>10</SWITCHBACKHBNUM>
				<BLKFLAG>0</BLKFLAG><!--Unblock-->
				<TSACK>200</TSACK>
				<DESCRI>Tash_BSC1_0/24/1</DESCRI>
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
				<VRFIDX>0</VRFIDX>
				<IPVERSION>0</IPVERSION><!--IPv4-->
				<MAXSCTPPDUSIZE>1464</MAXSCTPPDUSIZE>
				<DTLSPOLICYID>255</DTLSPOLICYID><!--NULL-->
			</attributes>
		</SCTPLNK>
	</class>\n"""
new_sctplnkUL = f"""	<class>
		<SCTPLNK>
			<attributes>
				<SCTPNO>2</SCTPNO>
				<CN>0</CN>
				<SRN>0</SRN>
				<SN>7</SN>
				<MAXSTREAM>17</MAXSTREAM>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<LOCIP>10.80.{oktet[2]}.{oktet[3]}</LOCIP>
				<SECLOCIP>0.0.0.0</SECLOCIP>
				<LOCPORT>1024</LOCPORT>
				<PEERIP>10.6.0.160</PEERIP>
				<SECPEERIP>0.0.0.0</SECPEERIP>
				<PEERPORT>36412</PEERPORT>
				<RTOMIN>1000</RTOMIN>
				<RTOMAX>3000</RTOMAX>
				<RTOINIT>1000</RTOINIT>
				<RTOALPHA>12</RTOALPHA>
				<RTOBETA>25</RTOBETA>
				<HBINTER>5000</HBINTER>
				<MAXASSOCRETR>10</MAXASSOCRETR>
				<MAXPATHRETR>5</MAXPATHRETR>
				<CHKSUMTYPE>1</CHKSUMTYPE><!--CRC32-->
				<AUTOSWITCH>1</AUTOSWITCH><!--Enable-->
				<SWITCHBACKHBNUM>10</SWITCHBACKHBNUM>
				<BLKFLAG>0</BLKFLAG><!--Unblock-->
				<TSACK>200</TSACK>
				<DESCRI></DESCRI>
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
				<VRFIDX>0</VRFIDX>
				<IPVERSION>0</IPVERSION><!--IPv4-->
				<MAXSCTPPDUSIZE>1464</MAXSCTPPDUSIZE>
				<DTLSPOLICYID>255</DTLSPOLICYID><!--NULL-->
			</attributes>
		</SCTPLNK>
		<SCTPLNK>
			<attributes>
				<SCTPNO>1</SCTPNO>
				<CN>0</CN>
				<SRN>0</SRN>
				<SN>7</SN>
				<MAXSTREAM>17</MAXSTREAM>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<LOCIP>10.75.{oktet[2]}.{oktet[3]}</LOCIP>
				<SECLOCIP>0.0.0.0</SECLOCIP>
				<LOCPORT>10002</LOCPORT>
				<PEERIP>10.150.1.149</PEERIP>
				<SECPEERIP>10.150.1.156</SECPEERIP>
				<PEERPORT>58080</PEERPORT>
				<RTOMIN>1000</RTOMIN>
				<RTOMAX>3000</RTOMAX>
				<RTOINIT>1000</RTOINIT>
				<RTOALPHA>12</RTOALPHA>
				<RTOBETA>25</RTOBETA>
				<HBINTER>5000</HBINTER>
				<MAXASSOCRETR>10</MAXASSOCRETR>
				<MAXPATHRETR>5</MAXPATHRETR>
				<CHKSUMTYPE>1</CHKSUMTYPE><!--CRC32-->
				<AUTOSWITCH>1</AUTOSWITCH><!--Enable-->
				<SWITCHBACKHBNUM>10</SWITCHBACKHBNUM>
				<BLKFLAG>0</BLKFLAG><!--Unblock-->
				<TSACK>200</TSACK>
				<DESCRI>Tash_RNC1_0/24/1</DESCRI>
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
				<VRFIDX>0</VRFIDX>
				<IPVERSION>0</IPVERSION><!--IPv4-->
				<MAXSCTPPDUSIZE>1464</MAXSCTPPDUSIZE>
				<DTLSPOLICYID>255</DTLSPOLICYID><!--NULL-->
			</attributes>
		</SCTPLNK>
		<SCTPLNK>
			<attributes>
				<SCTPNO>0</SCTPNO>
				<CN>0</CN>
				<SRN>0</SRN>
				<SN>7</SN>
				<MAXSTREAM>17</MAXSTREAM>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<LOCIP>10.75.{oktet[2]}.{oktet[3]}</LOCIP>
				<SECLOCIP>0.0.0.0</SECLOCIP>
				<LOCPORT>10001</LOCPORT>
				<PEERIP>10.150.1.149</PEERIP>
				<SECPEERIP>10.150.1.156</SECPEERIP>
				<PEERPORT>58080</PEERPORT>
				<RTOMIN>1000</RTOMIN>
				<RTOMAX>3000</RTOMAX>
				<RTOINIT>1000</RTOINIT>
				<RTOALPHA>12</RTOALPHA>
				<RTOBETA>25</RTOBETA>
				<HBINTER>5000</HBINTER>
				<MAXASSOCRETR>10</MAXASSOCRETR>
				<MAXPATHRETR>5</MAXPATHRETR>
				<CHKSUMTYPE>1</CHKSUMTYPE><!--CRC32-->
				<AUTOSWITCH>1</AUTOSWITCH><!--Enable-->
				<SWITCHBACKHBNUM>10</SWITCHBACKHBNUM>
				<BLKFLAG>0</BLKFLAG><!--Unblock-->
				<TSACK>200</TSACK>
				<DESCRI>Tash_RNC1_0/24/1</DESCRI>
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
				<VRFIDX>0</VRFIDX>
				<IPVERSION>0</IPVERSION><!--IPv4-->
				<MAXSCTPPDUSIZE>1464</MAXSCTPPDUSIZE>
				<DTLSPOLICYID>255</DTLSPOLICYID><!--NULL-->
			</attributes>
		</SCTPLNK>
	</class>\n"""

start_cpbearer = replacing.find("""	<class>
		<CPBEARER>""")
finish_cpbearer = replacing.find("""	<class>
		<IPSECBINDITF>""")
old_cpbearer = replacing[start_cpbearer:finish_cpbearer]
new_cpbearer = f"""	<class>
		<CPBEARER>
			<attributes>
				<CPBEARID>4</CPBEARID>
				<FLAG>0</FLAG><!--Master-->
				<BEARTYPE>1</BEARTYPE><!--SCTPLNK-->
				<LINKNO>3</LINKNO>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
			</attributes>
		</CPBEARER>
		<CPBEARER>
			<attributes>
				<CPBEARID>3</CPBEARID>
				<FLAG>0</FLAG><!--Master-->
				<BEARTYPE>1</BEARTYPE><!--SCTPLNK-->
				<LINKNO>2</LINKNO>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
			</attributes>
		</CPBEARER>
		<CPBEARER>
			<attributes>
				<CPBEARID>2</CPBEARID>
				<FLAG>0</FLAG><!--Master-->
				<BEARTYPE>1</BEARTYPE><!--SCTPLNK-->
				<LINKNO>1</LINKNO>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
			</attributes>
		</CPBEARER>
		<CPBEARER>
			<attributes>
				<CPBEARID>1</CPBEARID>
				<FLAG>0</FLAG><!--Master-->
				<BEARTYPE>1</BEARTYPE><!--SCTPLNK-->
				<LINKNO>0</LINKNO>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
			</attributes>
		</CPBEARER>
	</class>\n"""
new_cpbearerUL = f"""	<class>
		<CPBEARER>
			<attributes>
				<CPBEARID>2</CPBEARID>
				<FLAG>0</FLAG><!--Master-->
				<BEARTYPE>1</BEARTYPE><!--SCTPLNK-->
				<LINKNO>2</LINKNO>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
			</attributes>
		</CPBEARER>
		<CPBEARER>
			<attributes>
				<CPBEARID>1</CPBEARID>
				<FLAG>0</FLAG><!--Master-->
				<BEARTYPE>1</BEARTYPE><!--SCTPLNK-->
				<LINKNO>1</LINKNO>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
			</attributes>
		</CPBEARER>
		<CPBEARER>
			<attributes>
				<CPBEARID>0</CPBEARID>
				<FLAG>0</FLAG><!--Master-->
				<BEARTYPE>1</BEARTYPE><!--SCTPLNK-->
				<LINKNO>0</LINKNO>
				<CTRLMODE>0</CTRLMODE><!--Manual Mode-->
				<AUTOCFGFLAG>0</AUTOCFGFLAG><!--Manual Created-->
			</attributes>
		</CPBEARER>
	</class>\n"""

if Vibor == "0":
    replacing = replacing.replace(old_sctplnk, new_sctplnk)
    replacing = replacing.replace(old_cpbearer, new_cpbearer)

elif Vibor == "1":
    replacing = replacing.replace(old_sctplnk, new_sctplnkUL)
    replacing = replacing.replace(old_cpbearer, new_cpbearerUL)
else:
    print("НАПИСАНО же ЛИБО-0, ЛИБО-1, что непонятного ???")

start_USERPLANEPEER = replacing.find("""	<class>
		<USERPLANEPEER>""")
finish_USERPLANEPEER = replacing.find("""		</USERPLANEPEER>
	</class>""")
old_USERPLANEPEER= replacing[start_USERPLANEPEER:finish_USERPLANEPEER]
new_USERPLANEPEER = f""
replacing = replacing.replace(old_USERPLANEPEER, """""").replace("""
		</USERPLANEPEER>
	</class>""", "")

start_SCTPPEER = replacing.find("""	<class>
		<SCTPPEER>""")
finish_SCTPPEER = replacing.find("""		</SCTPPEER>
	</class>""")
old_SCTPPEER= replacing[start_SCTPPEER:finish_SCTPPEER]
new_SCTPPEER = f""
replacing = replacing.replace(old_SCTPPEER, """""").replace("""
		</SCTPPEER>
	</class>""", "")

start_SCTPPEERREFS = replacing.find("""				<SCTPPEERREFS>""")
finish_SCTPPEERREFS = replacing.find("""				</SCTPPEERREFS>
				<LOOSESCTPPEERREFS>""")
old_SCTPPEERREFS = replacing[start_SCTPPEERREFS:finish_SCTPPEERREFS]
new_SCTPPEERREFS = f""
replacing = replacing.replace(old_SCTPPEERREFS, """""").replace("""
				</SCTPPEERREFS>""", "")

start_USERPLANEPEERREFS = replacing.find("""				<USERPLANEPEERREFS>""")
finish_USERPLANEPEERREFS = replacing.find("""				</USERPLANEPEERREFS>
				<LOOSEUSERPLANEPEERREFS>""")
old_USERPLANEPEERREFS= replacing[start_USERPLANEPEERREFS:finish_USERPLANEPEERREFS]
new_USERPLANEPEERREFS = f""
replacing = replacing.replace(old_USERPLANEPEERREFS, """""").replace("""
				</USERPLANEPEERREFS>""", "")

start_EUTRANINTRAFREQNCELL= replacing.find("""	<class>
		<EutranExternalCell>""")
finish_EUTRANINTRAFREQNCELL = replacing.find("""		</UtranNCell>
	</class>""")
old_EUTRANINTRAFREQNCELL = replacing[start_EUTRANINTRAFREQNCELL:finish_EUTRANINTRAFREQNCELL]
new_EUTRANINTRAFREQNCELL = f""
replacing = replacing.replace(old_EUTRANINTRAFREQNCELL, "").replace("""
		</UtranNCell>
	</class>""", "")

start_X2Interface = replacing.find("""	<class>
		<X2Interface>""")
finish_X2Interface = replacing.find("""		</X2Interface>
	</class>""")
old_X2Interface = replacing[start_X2Interface:finish_X2Interface]
new_X2Interface = f""
replacing = replacing.replace(old_X2Interface, """""").replace("""
		</X2Interface>
	</class>""", "")

start_EutranExternalCellPlmn = replacing.find("""	<class>
		<EutranExternalCellPlmn>""")
finish_EutranExternalCellPlmn = replacing.find("""		</EutranExternalCellPlmn>
	</class>""")
old_EutranExternalCellPlmn = replacing[start_EutranExternalCellPlmn:finish_EutranExternalCellPlmn]
new_EutranExternalCellPlmn = f""
replacing = replacing.replace(old_EutranExternalCellPlmn, """	<class>
		<EutranExternalCellPlmn>
			<attributes>
			</attributes>\n""")

now2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

GOTOV = f"NEWCFGDATA_{now2}.xml"
Download = open(GOTOV, mode='x', encoding='utf-8')
Download.write(replacing)

path = os.getcwd()
print(path)
os.system(fr"explorer.exe {path}\NEWCFGDATA_{now2}.xml")
