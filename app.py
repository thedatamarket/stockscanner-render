from distutils.log import debug
from flask import Flask
from flask import render_template 
from bs4 import BeautifulSoup
import requests
import csv
import time
from datetime import datetime, date
from flask import request, make_response,redirect, url_for, Response
from lxml import etree
import yfinance as yf
import dropbox
import pandas as pd
import snscrape.modules.twitter as sntwitter

ticker = ["20MICRONS", "21STCENMGM", "3IINFOLTD", "3MINDIA", "3PLAND", "5PAISA", "63MOONS", "A2ZINFRA", "AAKASH", "AAREYDRUGS", "AARON", "AARTIDRUGS", "AARTIIND", "AARTISURF", "AARVEEDEN", "AARVI", "AAVAS", "ABAN", "ABB", "ABBOTINDIA", "ABCAPITAL", "ABFRL", "ABMINTLLTD", "ABSLAMC", "ACC", "ACCELYA", "ACCURACY", "ACE", "ACRYSIL", "ADANIENT", "ADANIGREEN", "ADANIPORTS", "ADANIPOWER", "ADANITRANS", "ADFFOODS", "ADL", "ADORWELD", "ADROITINFO", "ADSL", "ADVANIHOTR", "ADVENZYMES", "AEGISCHEM", "AFFLE", "AGARIND", "AGRITECH", "AGROPHOS", "AGSTRA", "AHLADA", "AHLEAST", "AHLUCONT", "AHLWEST", "AIAENG", "AIRAN", "AIROLAM", "AJANTPHARM", "AJMERA", "AJOONI", "AJRINFRA", "AKASH", "AKG", "AKSHARCHEM", "AKSHOPTFBR", "AKZOINDIA", "ALANKIT", "ALBERTDAVD", "ALEMBICLTD", "ALICON", "ALKALI", "ALKEM", "ALKYLAMINE", "ALLCARGO", "ALLSEC", "ALMONDZ", "ALOKINDS", "ALPA", "ALPHAGEO", "ALPSINDUS", "AMARAJABAT", "AMBER", "AMBICAAGAR", "AMBIKCO", "AMBUJACEM", "AMDIND", "AMIORG", "AMJLAND", "AMRUTANJAN", "ANANDRATHI", "ANANTRAJ", "ANDHRACEMT", "ANDHRAPAP", "ANDHRSUGAR", "ANDREWYU", "ANGELONE", "ANIKINDS", "ANKITMETAL", "ANMOL", "ANSALAPI", "ANSALHSG", "ANUP", "ANURAS", "APARINDS", "APCL", "APCOTEXIND", "APEX", "APLAPOLLO", "APLLTD", "APOLLO", "APOLLOHOSP", "APOLLOPIPE", "APOLLOTYRE", "APOLSINHOT", "APTECHT", "APTUS", "ARCHIDPLY", "ARCHIES", "ARENTERP", "ARIES", "ARIHANTCAP", "ARIHANTSUP", "ARMANFIN", "AROGRANITE", "ARROWGREEN", "ARSHIYA", "ARSSINFRA", "ARTEMISMED", "ARTNIRMAN", "ARVEE", "ARVIND", "ARVINDFASN", "ARVSMART", "ASAHIINDIA", "ASAHISONG", "ASAL", "ASALCBR", "ASHAPURMIN", "ASHIANA", "ASHIMASYN", "ASHOKA", "ASHOKLEY", "ASIANENE", "ASIANHOTNR", "ASIANPAINT", "ASIANTILES", "ASPINWALL", "ASTEC", "ASTERDM", "ASTRAL", "ASTRAMICRO", "ASTRAZEN", "ASTRON", "ATFL", "ATGL", "ATLANTA", "ATUL", "ATULAUTO", "AUBANK", "AURIONPRO", "AUROPHARMA", "AURUM", "AUSOMENT", "AUTOAXLES", "AUTOIND", "AVADHSUGAR", "AVANTIFEED", "AVTNPL", "AWHCL", "AWL", "AXISBANK", "AXISCADES", "AYMSYNTEX", "BAFNAPH", "BAGFILMS", "BAJAJ-AUTO", "BAJAJCON", "BAJAJELEC", "BAJAJFINSV", "BAJAJHCARE", "BAJAJHIND", "BAJAJHLDNG", "BAJFINANCE", "BALAJITELE", "BALAMINES", "BALAXI", "BALKRISHNA", "BALKRISIND", "BALLARPUR", "BALMLAWRIE", "BALPHARMA", "BALRAMCHIN", "BANARBEADS", "BANARISUG", "BANCOINDIA", "BANDHANBNK", "BANG", "BANKA", "BANKBARODA", "BANKINDIA", "BANSWRAS", "BARBEQUE", "BARTRONICS", "BASF", "BASML", "BATAINDIA", "BAYERCROP", "BBL", "BBOX", "BBTC", "BCG", "BCLIND", "BCONCEPTS", "BCP", "BDL", "BEARDSELL", "BECTORFOOD", "BEDMUTHA", "BEL", "BEML", "BEPL", "BERGEPAINT", "BESTAGRO", "BFINVEST", "BFUTILITIE", "BGLOBAL", "BGRENERGY", "BHAGCHEM", "BHAGERIA", "BHAGYANGR", "BHAGYAPROP", "BHANDARI", "BHARATFORG", "BHARATGEAR", "BHARATRAS", "BHARATWIRE", "BHARTIARTL", "BHEL", "BIGBLOC", "BIL", "BINDALAGRO", "BIOCON", "BIOFILCHEM", "BIRLACABLE", "BIRLACORPN", "BIRLAMONEY", "BIRLATYRE", "BKMINDST", "BLBLIMITED", "BLISSGVS", "BLKASHYAP", "BLS", "BLUECHIP", "BLUECOAST", "BLUEDART", "BLUESTARCO", "BODALCHEM", "BOMDYEING", "BOROLTD", "BORORENEW", "BOSCHLTD", "BPCL", "BPL", "BRFL", "BRIGADE", "BRITANNIA", "BRNL", "BROOKS", "BSE", "BSHSL", "BSL", "BSOFT", "BURNPUR", "BUTTERFLY", "BVCL", "BYKE", "CADILAHC", "CALSOFT", "CAMLINFINE", "CAMS", "CANBK", "CANDC", "CANFINHOME", "CANTABIL", "CAPACITE", "CAPLIPOINT", "CAPTRUST", "CARBORUNIV", "CAREERP", "CARERATING", "CARTRADE", "CASTROLIND", "CCHHL", "CCL", "CDSL", "CEATLTD", "CEBBCO", "CELEBRITY", "CENTENKA", "CENTEXT", "CENTRALBK", "CENTRUM", "CENTUM", "CENTURYPLY", "CENTURYTEX", "CERA", "CEREBRAINT", "CESC", "CGCL", "CGPOWER", "CHALET", "CHAMBLFERT", "CHEMBOND", "CHEMCON", "CHEMFAB", "CHEMPLASTS", "CHENNPETRO", "CHOLAFIN", "CHOLAHLDNG", "CIGNITITEC", "CINELINE", "CINEVISTA", "CIPLA", "CLEAN", "CLEDUCATE", "CLNINDIA", "CLSEL", "CMICABLES", "CMSINFO", "COALINDIA", "COASTCORP", "COCHINSHIP", "COFFEEDAY", "COFORGE", "COLPAL", "COMPINFO", "COMPUSOFT", "CONCOR", "CONFIPET", "CONSOFINVT", "CONTROLPR", "CORALFINAC", "CORDSCABLE", "COROMANDEL", "COSMOFILMS", "COUNCODOS", "CRAFTSMAN", "CREATIVE", "CREATIVEYE", "CREDITACC", "CREST", "CRISIL", "CROMPTON", "CROWN", "CSBBANK", "CTE", "CUB", "CUBEXTUB", "CUMMINSIND", "CUPID", "CYBERMEDIA", "CYBERTECH", "CYIENT", "DAAWAT", "DABUR", "DALALSTCOM", "DALBHARAT", "DALMIASUG", "DAMODARIND", "DANGEE", "DATAMATICS", "DATAPATTNS", "DBCORP", "DBL", "DBREALTY", "DBSTOCKBRO", "DCAL", "DCBBANK", "DCM", "DCMFINSERV", "DCMNVL", "DCMSHRIRAM", "DCMSRIND", "DCW", "DECCANCE", "DEEPAKFERT", "DEEPAKNTR", "DEEPENR", "DEEPINDS", "DELPHIFX", "DELTACORP", "DELTAMAGNT", "DEN", "DENORA", "DEVIT", "DEVYANI", "DFMFOODS", "DGCONTENT", "DHAMPURSUG", "DHANBANK", "DHANI", "DHANUKA", "DHARAMSI", "DHARSUGAR", "DHRUV", "DHUNINV", "DIAMONDYD", "DIAPOWER", "DICIND", "DIGISPICE", "DIGJAMLMTD", "DISHTV", "DIVISLAB", "DIXON", "DLF", "DLINKINDIA", "DMART", "DNAMEDIA", "DODLA", "DOLATALGO", "DOLLAR", "DONEAR", "DPABHUSHAN", "DPSCLTD", "DPWIRES", "DRCSYSTEMS", "DREDGECORP", "DRREDDY", "DSSL", "DTIL", "DUCON", "DVL", "DWARKESH", "DYNAMATECH", "DYNPRO", "EASEMYTRIP", "EASTSILK", "EASUNREYRL", "ECLERX", "EDELWEISS", "EDUCOMP", "EICHERMOT", "EIDPARRY", "EIFFL", "EIHAHOTELS", "EIHOTEL", "EIMCOELECO", "EKC", "ELECON", "ELECTCAST", "ELECTHERM", "ELGIEQUIP", "ELGIRUBCO", "EMAMILTD", "EMAMIPAP", "EMAMIREAL", "EMKAY", "EMMBI", "ENDURANCE", "ENERGYDEV", "ENGINERSIN", "ENIL", "EPL", "EQUIPPP", "EQUITAS", "EQUITASBNK", "ERIS", "EROSMEDIA", "ESABINDIA", "ESCORTS", "ESSARSHPNG", "ESTER", "EUROTEXIND", "EUROTEXIND", "EVEREADY", "EVERESTIND", "EXCEL", "EXCELINDUS", "EXIDEIND", "EXPLEOSOL", "EXXARO", "FACT", "FAIRCHEMOR", "FCL", "FCONSUMER", "FCSSOFT", "FDC", "FEDERALBNK", "FEL", "FELDVR", "FIBERWEB", "FIEMIND", "FILATEX", "FINCABLES", "FINEORG", "FINOPB", "FINPIPE", "FLEXITUFF", "FLFL", "FLUOROCHEM", "FMGOETZE", "FMNL", "FOCUS", "FOODSIN", "FORCEMOT", "FORTIS", "FOSECOIND", "FRETAIL", "FSC", "FSL", "GABRIEL", "GAEL", "GAIL", "GAL", "GALAXYSURF", "GALLANTT", "GALLISPAT", "GANDHITUBE", "GANECOS", "GANESHBE", "GANESHHOUC", "GANGAFORGE", "GANGESSECU", "GANGOTRI", "GARFIBRES", "GATI", "GAYAHWS", "GAYAPROJ", "GEECEE", "GEEKAYWIRE", "GENCON", "GENESYS", "GENUSPAPER", "GENUSPOWER", "GEOJITFSL", "GEPIL", "GESHIP", "GET&D", "GFLLIMITED", "GFSTEELS", "GHCL", "GICHSGFIN", "GICRE", "GILLANDERS", "GILLETTE", "GINNIFILA", "GIPCL", "GISOLUTION", "GKWLIMITED", "GLAND", "GLAXO", "GLENMARK", "GLFL", "GLOBAL", "GLOBALVECT", "GLOBE", "GLOBUSSPR", "GLS", "GMBREW", "GMDCLTD", "GMMPFAUDLR", "GMRINFRA", "GNA", "GNFC", "GOACARBON", "GOCLCORP", "GOCOLORS", "GODFRYPHLP", "GODHA", "GODREJAGRO", "GODREJCP", "GODREJIND", "GODREJPROP", "GOENKA", "GOKEX", "GOKUL", "GOKULAGRO", "GOLDENTOBC", "GOLDIAM", "GOLDTECH", "GOODLUCK", "GOODYEAR", "GPIL", "GPPL", "GPTINFRA", "GRANULES", "GRAPHITE", "GRASIM", "GRAUWEIL", "GRAVITA", "GREAVESCOT", "GREENLAM", "GREENPANEL", "GREENPLY", "GREENPOWER", "GRINDWELL", "GRINFRA", "GROBTEA", "GRPLTD", "GRSE", "GRWRHITECH", "GSCLCEMENT", "GSFC", "GSPL", "GSS", "GTL", "GTLINFRA", "GTPL", "GUFICBIO", "GUJALKALI", "GUJAPOLLO", "GUJGASLTD", "GUJRAFFIA", "GULFOILLUB", "GULFPETRO", "GULPOLY", "HAL", "HAPPSTMNDS", "HARRMALAYA", "HATHWAY", "HATSUN", "HAVELLS", "HAVISHA", "HBLPOWER", "HBSL", "HCC", "HCG", "HCL-INSYS", "HCLTECH", "HDFC", "HDFCAMC", "HDFCBANK", "HDFCLIFE", "HDIL", "HECPROJECT", "HEG", "HEIDELBERG", "HEMIPROP", "HERANBA", "HERCULES", "HERITGFOOD", "HEROMOTOCO", "HESTERBIO", "HEXATRADEX", "HFCL", "HGINFRA", "HGS", "HIKAL", "HIL", "HILTON", "HIMATSEIDE", "HINDALCO", "HINDCOMPOS", "HINDCON", "HINDCOPPER", "HINDMOTORS", "HINDNATGLS", "HINDOILEXP", "HINDPETRO", "HINDUNILVR", "HINDZINC", "HIRECT", "HISARMETAL", "HITECH", "HITECHCORP", "HITECHGEAR", "HLEGLAS", "HLVLTD", "HMT", "HMVL", "HNDFDS", "HOMEFIRST", "HONAUT", "HONDAPOWER", "HOTELRUGBY", "HOVS", "HPAL", "HPL", "HSCL", "HSIL", "HTMEDIA", "HUBTOWN", "HUDCO", "HUHTAMAKI", "IBREALEST", "IBULHSGFIN", "ICDSLTD", "ICEMAKE", "ICICIBANK", "ICICIGI", "ICICIPRULI", "ICIL", "ICRA", "IDBI", "IDEA", "IDFC", "IDFCFIRSTB", "IEX", "IFBAGRO", "IFBIND", "IFCI", "IFGLEXPOR", "IGARASHI", "IGL", "IGPL", "IIFL", "IIFLSEC", "IIFLWAM", "IITL", "IL&FSENGG", "IL&FSTRANS", "IMAGICAA", "IMFA", "IMPAL", "IMPEXFERRO", "INCREDIBLE", "INDBANK", "INDHOTEL", "INDIACEM", "INDIAGLYCO", "INDIAMART", "INDIANB", "INDIANCARD", "INDIANHUME", "INDIGO", "INDIGOPNTS", "INDLMETER", "INDNIPPON", "INDOCO", "INDORAMA", "INDOSOLAR", "INDOSTAR", "INDOTECH", "INDOTHAI", "INDOWIND", "INDRAMEDCO", "INDSWFTLAB", "INDSWFTLTD", "INDTERRAIN", "INDUSINDBK", "INDUSTOWER", "INEOSSTYRO", "INFIBEAM", "INFOBEAN", "INFOMEDIA", "INFY", "INGERRAND", "INOXLEISUR", "INOXWIND", "INSECTICID", "INSPIRISYS", "INTEGRA", "INTELLECT", "INTENTECH", "INTLCONV", "INVENTURE", "IOB", "IOC", "IOLCP", "IPCALAB", "IPL", "IRB", "IRCON", "IRCTC", "IRFC", "IRIS", "IRISDOREME", "ISEC", "ISFT", "ISGEC", "ISMTLTD", "ITC", "ITDC", "ITDCEM", "ITI", "IVC", "IVP", "IWEL", "IZMO", "J&KBANK", "JAGRAN", "JAGSNPHARM", "JAIBALAJI", "JAICORPLTD", "JAINSTUDIO", "JAIPURKURT", "JAMNAAUTO", "JASH", "JAYAGROGN", "JAYBARMARU", "JAYNECOIND", "JAYSREETEA", "JBCHEPHARM", "JBFIND", "JBMA", "JCHAC", "JETAIRWAYS", "JETFREIGHT", "JHS", "JIKIND", "JINDALPHOT", "JINDALPOLY", "JINDALSAW", "JINDALSTEL", "JINDCOT", "JINDRILL", "JINDWORLD", "JISLDVREQS", "JISLJALEQS", "JITFINFRA", "JIYAECO", "JKCEMENT", "JKIL", "JKLAKSHMI", "JKPAPER", "JKTYRE", "JMA", "JMCPROJECT", "JMFINANCIL", "JMTAUTOLTD", "JOCIL", "JPASSOCIAT", "JPINFRATEC", "JPOLYINVST", "JPPOWER", "JSL", "JSLHISAR", "JSWENERGY", "JSWHL", "JSWISPL", "JSWSTEEL", "JTEKTINDIA", "JTLINFRA", "JUBLFOOD", "JUBLINDS", "JUBLINGREA", "JUBLPHARMA", "JUSTDIAL", "JYOTHYLAB", "JYOTISTRUC", "KABRAEXTRU", "KAJARIACER", "KAKATCEM", "KALPATPOWR", "KALYANI", "KALYANIFRG", "KALYANKJIL", "KAMATHOTEL", "KAMDHENU", "KANANIIND", "KANORICHEM", "KANPRPLA", "KANSAINER", "KAPSTON", "KARMAENG", "KARURVYSYA", "KAUSHALYA", "KAVVERITEL", "KAYA", "KBCGLOBAL", "KCP", "KCPSUGIND", "KDDL", "KEC", "KECL", "KEERTI", "KEI", "KELLTONTEC", "KENNAMET", "KERNEX", "KESORAMIND", "KEYFINSERV", "KHADIM", "KHAICHEM", "KHAITANLTD", "KHANDSE", "KICL", "KILITCH", "KIMS", "KINGFA", "KIOCL", "KIRIINDUS", "KIRLFER", "KIRLOSBROS", "KIRLOSENG", "KIRLOSIND", "KITEX", "KKCL", "KMSUGAR", "KNRCON", "KOKUYOCMLN", "KOLTEPATIL", "KOPRAN", "KOTAKBANK", "KOTARISUG", "KOTHARIPET", "KOTHARIPRO", "KOVAI", "KPIGLOBAL", "KPITTECH", "KPRMILL", "KRBL", "KREBSBIO", "KRIDHANINF", "KRISHANA", "KRITI", "KRSNAA", "KSB", "KSCL", "KSL", "KTKBANK", "KUANTUM", "L&TFH", "LAGNAM", "LAKPRE", "LALPATHLAB", "LAMBODHARA", "LAOPALA", "LASA", "LATENTVIEW", "LAURUSLABS", "LAXMICOT", "LAXMIMACH", "LCCINFOTEC", "LEMONTREE", "LFIC", "LGBBROSLTD", "LGBFORGE", "LIBAS", "LIBERTSHOE", "LICHSGFIN", "LIKHITHA", "LINC", "LINCOLN", "LINDEINDIA", "LODHA", "LOKESHMACH", "LOTUSEYE", "LOVABLE", "LPDC", "LSIL", "LT", "LTI", "LTTS", "LUMAXIND", "LUMAXTECH", "LUPIN", "LUXIND", "LXCHEM", "LYKALABS", "LYPSAGEMS", "M&M", "M&MFIN", "MAANALU", "MACPOWER", "MADHAV", "MADHUCON", "MADRASFERT", "MAGADSUGAR", "MAGNUM", "MAHABANK", "MAHAPEXLTD", "MAHASTEEL", "MAHEPC", "MAHESHWARI", "MAHINDCIE", "MAHLIFE", "MAHLOG", "MAHSCOOTER", "MAHSEAMLES", "MAITHANALL", "MALLCOM", "MALUPAPER", "MANAKALUCO", "MANAKCOAT", "MANAKSIA", "MANAKSTEEL", "MANALIPETC", "MANAPPURAM", "MANGALAM", "MANGCHEFER", "MANGLMCEM", "MANINDS", "MANINFRA", "MANORG", "MANUGRAPH", "MANYAVAR", "MAPMYINDIA", "MARALOVER", "MARATHON", "MARICO", "MARINE", "MARKSANS", "MARSHALL", "MARUTI", "MASFIN", "MASKINVEST", "MASTEK", "MATRIMONY", "MAWANASUG", "MAXHEALTH", "MAXIND", "MAXVIL", "MAYURUNIQ", "MAZDA", "MAZDOCK", "MBAPL", "MBECL", "MBLINFRA", "MCDOWELL-N", "MCL", "MCLEODRUSS", "MCX", "MEDICAMEQ", "MEDPLUS", "MEGASOFT", "MEGASTAR", "MELSTAR", "MENONBE", "MEP", "MERCATOR", "METALFORGE", "METROBRAND", "METROPOLIS", "MFL", "MFSL", "MGEL", "MGL", "MHLXMIRU", "MHRIL", "MICEL", "MIDHANI", "MINDACORP", "MINDAIND", "MINDTECK", "MINDTREE", "MIRCELECTR", "MIRZAINT", "MITTAL", "MMFL", "MMP", "MMTC", "MODIRUBBER", "MODISNME", "MOHITIND", "MOHOTAIND", "MOIL", "MOKSH", "MOL", "MOLDTECH", "MOLDTKPAC", "MONARCH", "MONTECARLO", "MORARJEE", "MOREPENLAB", "MOTHERSUMI", "MOTILALOFS", "MOTOGENFIN", "MPHASIS", "MPSLTD", "MRF", "MRO-TEK", "MRPL", "MSPL", "MSTCLTD", "MTARTECH", "MTEDUCARE", "MTNL", "MUKANDENGG", "MUKANDLTD", "MUKTAARTS", "MUNJALAU", "MUNJALSHOW", "MURUDCERA", "MUTHOOTCAP", "MUTHOOTFIN", "NACLIND", "NAGAFERT", "NAGREEKCAP", "NAGREEKEXP", "NAHARCAP", "NAHARINDUS", "NAHARPOLY", "NAHARSPING", "NAM-INDIA", "NATCOPHARM", "NATHBIOGEN", "NATIONALUM", "NATNLSTEEL", "NAUKRI", "NAVINFLUOR", "NAVKARCORP", "NAVNETEDUL", "NAZARA", "NBCC", "NBIFIN", "NBVENTURES", "NCC", "NCLIND", "NDGL", "NDL", "NDRAUTO", "NDTV", "NECCLTD", "NECLIFE", "NELCAST", "NELCO", "NEOGEN", "NESCO", "NESTLEIND", "NETWORK18", "NEULANDLAB", "NEWGEN", "NEXTMEDIA", "NFL", "NGIL", "NH", "NHPC", "NIACL", "NIBL", "NIITLTD", "NILAINFRA", "NILASPACES", "NILKAMAL", "NIPPOBATRY", "NIRAJ", "NIRAJISPAT", "NITCO", "NITINSPIN", "NITIRAJ", "NKIND", "NLCINDIA", "NMDC", "NOCIL", "NOIDATOLL", "NORBTEAEXP", "NOVARTIND", "NRAIL", "NRBBEARING", "NSIL", "NTPC", "NUCLEUS", "NURECA", "NUVOCO", "NXTDIGITAL", "NYKAA", "OAL", "OBEROIRLTY", "OCCL", "OFSS", "OIL", "OILCOUNTUB", "OLECTRA", "OMAXAUTO", "OMAXE", "OMINFRAL", "OMKARCHEM", "ONELIFECAP", "ONEPOINT", "ONGC", "ONMOBILE", "ONWARDTEC", "OPTIEMUS", "OPTOCIRCUI", "ORBTEXP", "ORCHPHARMA", "ORICONENT", "ORIENTABRA", "ORIENTALTL", "ORIENTBELL", "ORIENTCEM", "ORIENTELEC", "ORIENTHOT", "ORIENTLTD", "ORIENTPPR", "ORISSAMINE", "ORTEL", "ORTINLAB", "OSWALAGRO", "PAEL", "PAGEIND", "PAISALO", "PALASHSECU", "PALREDTEC", "PANACEABIO", "PANACHE", "PANAMAPET", "PANSARI", "PAR", "PARACABLES", "PARAGMILK", "PARAS", "PARSVNATH", "PASUPTAC", "PATELENG", "PATINTLOG", "PAYTM", "PBAINFRA", "PCBL", "PCJEWELLER", "PDMJEPAPER", "PDPL", "PDSL", "PEARLPOLY", "PEL", "PENIND", "PENINLAND", "PERSISTENT", "PETRONET", "PFC", "PFIZER", "PFOCUS", "PFS", "PGEL", "PGHH", "PGHL", "PGIL", "PHOENIXLTD", "PIDILITIND", "PIIND", "PILANIINVS", "PILITA", "PIONDIST", "PIONEEREMB", "PITTIENG", "PKTEA", "PLASTIBLEN", "PNB", "PNBGILTS", "PNBHOUSING", "PNC", "PNCINFRA", "PODDARHOUS", "PODDARMENT", "POKARNA", "POLICYBZR", "POLYCAB", "POLYMED", "POLYPLEX", "PONNIERODE", "POONAWALLA", "POWERGRID", "POWERINDIA", "POWERMECH", "PPAP", "PPL", "PRAENG", "PRAJIND", "PRAKASH", "PRAKASHSTL", "PRAXIS", "PRECAM", "PRECOT", "PRECWIRE", "PREMEXPLN", "PREMIER", "PREMIERPOL", "PRESSMN", "PRESTIGE", "PRICOLLTD", "PRIMESECU", "PRINCEPIPE", "PRITIKAUTO", "PRIVISCL", "PROZONINTU", "PRSMJOHNSN", "PSB", "PSPPROJECT", "PTC", "PTL", "PUNJABCHEM", "PUNJLLOYD", "PURVA", "PVP", "PVR", "QUESS", "QUICKHEAL", "QUINTEGRA", "RADAAN", "RADICO", "RADIOCITY", "RAILTEL", "RAIN", "RAJESHEXPO", "RAJMET", "RAJRATAN", "RAJSREESUG", "RAJTV", "RAJVIR", "RALLIS", "RAMANEWS", "RAMASTEEL", "RAMCOCEM", "RAMCOIND", "RAMCOSYS", "RAMKY", "RANASUG", "RANEENGINE", "RANEHOLDIN", "RATEGAIN", "RATNAMANI", "RAYMOND", "RBA", "RBL", "RBLBANK", "RCF", "RCOM", "RECLTD", "REDINGTON", "REFEX", "REGENCERAM", "RELAXO", "RELCAPITAL", "RELIANCE", "RELIGARE", "RELINFRA", "REMSONSIND", "RENUKA", "REPCOHOME", "REPL", "REPRO", "RESPONIND", "REVATHI", "RGL", "RHFL", "RHIM", "RICOAUTO", "RIIL", "RITES", "RKDL", "RKEC", "RKFORGE", "RMCL", "RML", "RNAVAL", "ROHITFERRO", "ROHLTD", "ROLEXRINGS", "ROLLT", "ROLTA", "ROML", "ROSSARI", "ROSSELLIND", "ROUTE", "RPGLIFE", "RPOWER", "RPPINFRA", "RPPL", "RPSGVENT", "RSSOFTWARE", "RSWM", "RSYSTEMS", "RTNINDIA", "RTNPOWER", "RUBYMILLS", "RUCHI", "RUCHINFRA", "RUCHIRA", "RUPA", "RUSHIL", "RVHL", "RVNL", "S&SPOWER", "SABEVENTS", "SABTN", "SADBHAV", "SADBHIN", "SAFARI", "SAGARDEEP", "SAGCEM", "SAIL", "SAKAR", "SAKHTISUG", "SAKSOFT", "SAKUMA", "SALASAR", "SALONA", "SALSTEEL", "SALZERELEC", "SAMBHAAV", "SANCO", "SANDESH", "SANDHAR", "SANGAMIND", "SANGHIIND", "SANGHVIMOV", "SANGINITA", "SANOFI", "SANSERA", "SANWARIA", "SAPPHIRE", "SARDAEN", "SAREGAMA", "SARLAPOLY", "SASKEN", "SASTASUNDR", "SATHAISPAT", "SATIA", "SATIN", "SBC", "SBCL", "SBICARD", "SBILIFE", "SBIN", "SCAPDVR", "SCHAEFFLER", "SCHAND", "SCHNEIDER", "SCI", "SDBL", "SEAMECLTD", "SECURKLOUD", "SEJALLTD", "SELAN", "SELMC", "SEPOWER", "SEQUENT", "SERVOTECH", "SESHAPAPER", "SETCO", "SETUINFRA", "SEYAIND", "SFL", "SGIL", "SGL", "SHAHALLOYS", "SHAKTIPUMP", "SHALBY", "SHALPAINTS", "SHANKARA", "SHANTI", "SHANTIGEAR", "SHARDACROP", "SHARDAMOTR", "SHAREINDIA", "SHEMAROO", "SHIL", "SHILPAMED", "SHIVALIK", "SHIVAMAUTO", "SHIVAMILLS", "SHIVATEX", "SHK", "SHOPERSTOP", "SHRADHA", "SHREDIGCEM", "SHREECEM", "SHREEPUSHK", "SHREERAMA", "SHRENIK", "SHREYANIND", "SHREYAS", "SHRIPISTON", "SHRIRAMCIT", "SHRIRAMEPC", "SHRIRAMPPS", "SHYAMCENT", "SHYAMMETL", "SHYAMTEL", "SICAL", "SIEMENS", "SIGACHI", "SIGIND", "SIKKO", "SIL", "SILGO", "SILINV", "SILLYMONKS", "SIMBHALS", "SIMPLEXINF", "SINTERCOM", "SINTEX", "SIRCA", "SIS", "SITINET", "SIYSIL", "SJS", "SJVN", "SKFINDIA", "SKIL", "SKIPPER", "SKMEGGPROD", "SMARTLINK", "SMCGLOBAL", "SMLISUZU", "SMLT", "SMSLIFE", "SMSPHARMA", "SNOWMAN", "SOBHA", "SOLARA", "SOLARINDS", "SOMANYCERA", "SOMATEX", "SOMICONVEY", "SONACOMS", "SONATSOFTW", "SORILINFRA", "SOTL", "SOUTHBANK", "SOUTHWEST", "SPAL", "SPANDANA", "SPARC", "SPCENET", "SPECIALITY", "SPENCERS", "SPENTEX", "SPIC", "SPICEJET", "SPLIL", "SPMLINFRA", "SPTL", "SPYL", "SREEL", "SREINFRA", "SRF", "SRHHYPOLTD", "SRPL", "SRTRANSFIN", "SSWL", "STAMPEDE", "STAR", "STARCEMENT", "STARHEALTH", "STARPAPER", "STCINDIA", "STEELCAS", "STEELCITY", "STEELXIND", "STEL", "STERTOOLS", "STLTECH", "STOVEKRAFT", "STYLAMIND", "SUBCAPCITY", "SUBEXLTD", "SUBROS", "SUDARSCHEM", "SUMEETINDS", "SUMICHEM", "SUMIT", "SUMMITSEC", "SUNCLAYLTD", "SUNDARAM", "SUNDARMFIN", "SUNDARMHLD", "SUNDRMBRAK", "SUNDRMFAST", "SUNFLAG", "SUNPHARMA", "SUNTECK", "SUNTV", "SUPERHOUSE", "SUPERSPIN", "SUPPETRO", "SUPRAJIT", "SUPREMEENG", "SUPREMEIND", "SUPREMEINF", "SUPRIYA", "SURANASOL", "SURANAT&P", "SURYALAXMI", "SURYAROSNI", "SURYODAY", "SUTLEJTEX", "SUULD", "SUVEN", "SUVENPHAR", "SUVIDHAA", "SUZLON", "SVPGLOB", "SWANENERGY", "SWARAJENG", "SWELECTES", "SWSOLAR", "SYMPHONY", "SYNGENE", "TAINWALCHM", "TAJGVK", "TAKE", "TALBROAUTO", "TANLA", "TANTIACONS", "TARAPUR", "TARC", "TARMAT", "TARSONS", "TASTYBITE", "TATACHEM", "TATACOFFEE", "TATACOMM", "TATACONSUM", "TATAELXSI", "TATAINVEST", "TATAMETALI", "TATAMOTORS", "TATAMTRDVR", "TATAPOWER", "TATASTEEL", "TATASTLLP", "TATVA", "TBZ", "TCI", "TCIDEVELOP", "TCIEXP", "TCIFINANCE", "TCNSBRANDS", "TCPLPACK", "TCS", "TDPOWERSYS", "TEAMLEASE", "TECHIN", "TECHM", "TECHNOE", "TEGA", "TEJASNET", "TEMBO", "TERASOFT", "TEXINFRA", "TEXMOPIPES", "TEXRAIL", "TFCILTD", "TFL", "TGBHOTELS", "THANGAMAYL", "THEINVEST", "THEMISMED", "THERMAX", "THOMASCOOK", "THOMASCOTT", "THYROCARE", "TI", "TIDEWATER", "TIIL", "TIINDIA", "TIJARIA", "TIL", "TIMESGTY", "TIMETECHNO", "TIMKEN", "TINPLATE", "TIPSINDLTD", "TIRUMALCHM", "TIRUPATIFL", "TITAN", "TMRVL", "TNPETRO", "TNPL", "TNTELE", "TOKYOPLAST", "TORNTPHARM", "TORNTPOWER", "TOTAL", "TOUCHWOOD", "TPLPLASTEH", "TREEHOUSE", "TREJHARA", "TRENT", "TRF", "TRIDENT", "TRIGYN", "TRIL", "TRITURBINE", "TRIVENI", "TTKHLTCARE", "TTKPRESTIG", "TTL", "TTML", "TV18BRDCST", "TVSELECT", "TVSMOTOR", "TVSSRICHAK", "TVTODAY", "TVVISION", "TWL", "UBL", "UCALFUEL", "UCOBANK", "UDAICEMENT", "UFLEX", "UFO", "UGARSUGAR", "UGROCAP", "UJAAS", "UJJIVAN", "UJJIVANSFB", "ULTRACEMCO", "UMANGDAIRY", "UMESLTD", "UNICHEMLAB", "UNIDT", "UNIENTER", "UNIINFO", "UNIONBANK", "UNITECH", "UNITEDPOLY", "UNITEDTEA", "UNIVASTU", "UNIVCABLES", "UNIVPHOTO", "UPL", "URJA", "USHAMART", "UTIAMC", "UTTAMSTL", "UTTAMSUGAR", "V2RETAIL", "VADILALIND", "VAIBHAVGBL", "VAISHALI", "VAKRANGEE", "VALIANTORG", "VARDHACRLC", "VARDMNPOLY", "VARROC", "VASCONEQ", "VASWANI", "VBL", "VEDL", "VENKEYS", "VENUSREM", "VERTOZ", "VESUVIUS", "VETO", "VGUARD", "VHL", "VICEROY", "VIDHIING", "VIJAYA", "VIJIFIN", "VIKASECO", "VIKASLIFE", "VIKASPROP", "VIKASWSP", "VIMTALABS", "VINATIORGA", "VINDHYATEL", "VINEETLAB", "VINYLINDIA", "VIPCLOTHNG", "VIPIND", "VIPULLTD", "VISAKAIND", "VISASTEEL", "VISESHINFO", "VISHAL", "VISHNU", "VISHWARAJ", "VIVIDHA", "VIVIMEDLAB", "VLIFEPP", "VLSFINANCE", "VMART", "VOLTAMP", "VOLTAS", "VRLLOG", "VSSL", "VSTIND", "VSTTILLERS", "VTL", "WABAG", "WABCOINDIA", "WALCHANNAG", "WANBURY", "WATERBASE", "WEALTH", "WEBELSOLAR", "WEIZMANIND", "WELCORP", "WELENT", "WELINV", "WELSPUNIND", "WENDT", "WESTLIFE", "WFL", "WHEELS", "WHIRLPOOL", "WILLAMAGOR", "WINDLAS", "WINDMACHIN", "WINPRO", "WIPL", "WIPRO", "WOCKPHARMA", "WONDERLA", "WORTH", "WSI", "WSTCSTPAPR", "XCHANGING", "XELPMOC", "XPROINDIA", "YAARI", "YESBANK", "YUKEN", "ZEEL", "ZEELEARN", "ZEEMEDIA", "ZENITHEXPO", "ZENITHSTL", "ZENSARTECH", "ZENTEC", "ZODIAC", "ZODIACLOTH", "ZOMATO", "ZOTA", "ZUARI", "ZUARIGLOB", "ZYDUSWELL"] 

app = Flask(__name__,template_folder='template')

@app.route('/')
def stockNews1():
    return render_template('index.html')
    
@app.route('/data') 
def data():
    # df = pd.read_csv(r'C:\Users\tanmo\Desktop\flaskProject\webPage\Output\stock_15032022.csv')
    dbx = dropbox.Dropbox("NVwGrPvFLxgAAAAAAAAAAVUBiyewqJ5KTDlXkSBRNBBsH2-aZ9iKQvRkP1bIDy_G")
    now = datetime.now()
    dropbox_path= "/StockPriceDayChange/" + str(now.strftime("%d%m%Y")) + '.csv'
    result = dbx.files_get_temporary_link(dropbox_path)
    print(result.link)


    df = pd.read_csv(result.link, encoding= 'unicode_escape')
    return df.to_html()
 
@app.route('/index') 
def recentIndex():
    return render_template('recent.html', users1=ticker)

@app.route('/index1') 
def allnewsIndex():
    return render_template('allnews.html', users1=ticker)

@app.route('/<name>')
def stockNews(name):
    url = 'https://www.google.com/finance/quote/' + name + ':NSE'
    r = requests.get(url) 
    web_c1 = BeautifulSoup(r.text,'lxml')
    web_c1 = web_c1.findAll('div',class_='z4rs2b')
    news = []    
    for div in web_c1:
        web_c = div.find()
        time = web_c.find('div',class_='Adak').text
        web_c = web_c.find('div',class_='Tfehrf')
        web_c = web_c.find('div',class_='Yfwt5').text
        news.append(web_c + ' ' + time)
        # text = "\n".join(news)
    return render_template('headLines.html', users1=news)


@app.route('/news/<name>')
def allNews(name):
    url = 'https://news.google.com/search?q=' + name
    r = requests.get(url) 
    web_c1 = BeautifulSoup(r.text,'lxml')
    web_c1 = web_c1.findAll('div',class_='xrnccd')
    # print(web_c1)
    news = []    
    recent = []
    for div in web_c1:
      try:
        # print(div.find().text)
        div1 = div.find('h3',class_='ipQwMb ekueJc RD0gLb').text
        time = div.find('div',class_='SVJrMe')
        time = div.find('time',class_='WW6dff uQIVzc Sksgp slhocf').text
        text = div1 + ' ' + time
        news.append(text)
        if("hours" in text):
            recent.append(text)
      except:
        continue
    return render_template('headLines.html', users1=news)


@app.route("/button", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            pass # do something
        elif  request.form.get('action2') == 'VALUE2':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('button.html')
    
    return render_template("recent.html")


@app.route('/niftyindices')
def niftyindices():
    lst = []
    nifty = ["NIFTY_BANK", "NIFTY_AUTO", "NIFTY_FIN_SERVICE", "NIFTY_FMCG", "NIFTY_IT","NIFTY_MEDIA","NIFTY_METAL","NIFTY_PHARMA",  "NIFTY_PSU_BANK","NIFTY_PVT_BANK","NIFTY_REALTY","NIFTY_50","NIFTY_NEXT_50","NIFTY_100","NIFTY_200","NIFTY_500","NIFTY_MIDCAP_50",
          "INDIA_VIX"]
    df = pd.DataFrame(columns=["Index", "Change"])
    for i in nifty:
        url = 'https://www.google.com/finance/quote/' + i + ':INDEXNSE'
        r = requests.get(url) 
        web_c1 = BeautifulSoup(r.text,'lxml')
        info = web_c1.findAll('div',class_='P6K39c')
        prevClose = float(info[0].text.replace(",",""))
        currentPrice = float(web_c1.find('div',class_='YMlKec fxKbKc').text.replace(",",""))
        diff = (((currentPrice-prevClose)/prevClose)*100)
        print(i,round(diff,3))
        lst.append(i + " -----> " + str(round(diff,3)) + "%")
        df1 = pd.DataFrame(data=[[i,float(round(diff,3))]],columns=["Index", "Change"])
        df = pd.concat([df,df1], axis=0)
    # return render_template('niftyindices.html', users1=lst)
    df = df.sort_values(by=['Change'], ascending=False)
    return df.to_html()

@app.route('/change')
def stockpricechange():
    def percent(a,b):
        return (((a-b)/b)*100)
    def msg(message):
        # news = message.replace("(","").replace(")","").replace(".",",").replace("-","/")
        bot_token = '5041715929:AAFcraPI9-8jZR0bLkquRDNUXg96tEUKje4'
        bot_chatID = '1259144189'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id='+ bot_chatID + '&parse_mode=MarkdownV2&text=' + message

        response = requests.get(send_text)
        print(response.json())
        return response.json()
    now = datetime.now()
    file1 = str(now.strftime("%d%m%Y"))

    filename = 'Output/' + file1 + '.csv'
    with open(filename, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Price"])

    # ticker = ["ZOMATO", "ZOTA", "ZUARI", "ZUARIGLOB", "ZYDUSWELL"]
    for i in ticker:
        try:
            msg = []
            tik = i + '.NS'
            data = yf.download(tickers=tik, period='3d', interval='1d')
            data.reset_index(level=0, inplace=True)
            presentOpen  = data.iloc[-2]['Close']
            presentClose = data.iloc[-1]['Close']
            # week_1_change = data.iloc[-6]['Close']
            # month_1_change = data.iloc[-21]['Open']
            day_1 = percent(presentClose,presentOpen)
            print(day_1) 
            with open(filename, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i, day_1])
            print("{} ---> {}".format(i,day_1))
        except:
            time.sleep(2)
            continue
    dropbox_access_token= "NVwGrPvFLxgAAAAAAAAAAVUBiyewqJ5KTDlXkSBRNBBsH2-aZ9iKQvRkP1bIDy_G"    #Enter your own access token
    dropbox_path= "/StockPriceDayChange/" + file1 + '.csv'
    computer_path= filename
    
    client = dropbox.Dropbox(dropbox_access_token)
    print("[SUCCESS] dropbox account linked")
    # client.files_delete(dropbox_path)
    client.files_upload(open(computer_path, "rb").read(), dropbox_path)
    print("[UPLOADED] {}".format(computer_path))
    txt ="Unloaded in Dropbox Please Check"
    bot_token = '5041715929:AAFcraPI9-8jZR0bLkquRDNUXg96tEUKje4'
    bot_chatID = '1259144189'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id='+ bot_chatID + '&parse_mode=MarkdownV2&text=' + txt
    response = requests.get(send_text)
    print(response.json())



    dbx = dropbox.Dropbox("NVwGrPvFLxgAAAAAAAAAAVUBiyewqJ5KTDlXkSBRNBBsH2-aZ9iKQvRkP1bIDy_G")
    # filePath = "/output/18122021011000.csv"
    result = dbx.files_get_temporary_link(dropbox_path)
    print(result.link)
    return render_template('dayChange.html')


@app.route('/recent/<name>')
def recentNews1(name):
    url = 'https://news.google.com/search?q=' + name
    r = requests.get(url) 
    web_c1 = BeautifulSoup(r.text,'lxml')
    web_c1 = web_c1.findAll('div',class_='xrnccd')
    # print(web_c1)
    news = []    
    recent = []
    df = pd.DataFrame(columns=["News", "Time"])
    for div in web_c1:
      try:
        # print(div.find().text)
        div1 = div.find('h3',class_='ipQwMb ekueJc RD0gLb').text
        time = div.find('div',class_='SVJrMe')
        time = div.find('time',class_='WW6dff uQIVzc Sksgp slhocf').text
        text = div1 + ' ' + time
        news.append(text)
        if("hours" in time or "Yesterday" in time and "days" not in time):
            df1 = pd.DataFrame(data=[[div1,time]],columns=["News", "Time"])
            df = pd.concat([df,df1], axis=0)
            df = df.sort_values(by=['Time'], ascending=True)
      except:
        continue
    if(len(news) != 0):
        return df.to_html()
    else:
        return "<a>Sorry!! No recent news. Check 'All News'</p><br>"


@app.route('/mfchange')
def listmfchange():
    client = dropbox.Dropbox("NVwGrPvFLxgAAAAAAAAAAVUBiyewqJ5KTDlXkSBRNBBsH2-aZ9iKQvRkP1bIDy_G")
    mf_list = []
    def all_files_from_folder(folder):
        metadata = client.files_list_folder(folder)
        while True:
            for entry in metadata.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    yield entry
            if not metadata.has_more:
                break
            metadata = client.files_list_folder_continue(metadata.cursor)

    for i in all_files_from_folder("/results"):
        # print(i.path_lower.split("/")[-1])
        mf_list.append(i.path_lower.split("/")[-1])
        # mf_list.append(i.path_lower)
    return render_template('mf_list.html', users1=mf_list)

@app.route('/stockchange')
def liststockchange():
    client = dropbox.Dropbox("NVwGrPvFLxgAAAAAAAAAAVUBiyewqJ5KTDlXkSBRNBBsH2-aZ9iKQvRkP1bIDy_G")
    mf_list = []
    def all_files_from_folder(folder):
        metadata = client.files_list_folder(folder)
        while True:
            for entry in metadata.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    yield entry
            if not metadata.has_more:
                break
            metadata = client.files_list_folder_continue(metadata.cursor)

    for i in all_files_from_folder("/StockPriceDayChange"):
        # print(i.path_lower.split("/")[-1])
        mf_list.append(i.path_lower.split("/")[-1])
        # mf_list.append(i.path_lower)
    return render_template('stock_list.html', users1=mf_list)

@app.route('/data/stock/<name>') 
def StockData1(name):
    # df = pd.read_csv(r'C:\Users\tanmo\Desktop\flaskProject\webPage\Output\stock_15032022.csv')
    dbx = dropbox.Dropbox("NVwGrPvFLxgAAAAAAAAAAVUBiyewqJ5KTDlXkSBRNBBsH2-aZ9iKQvRkP1bIDy_G")
    query_list = 'https://indianstockscanner-pre.herokuapp.com//stockchange'
    dropbox_path= "/StockPriceDayChange/" + str(name)
    result = dbx.files_get_temporary_link(dropbox_path)
    print(result.link)
    df = pd.read_csv(result.link, encoding= 'unicode_escape')
    df = df.sort_values(by=['Price'], ascending=False)
    #return df.to_html()
    return render_template('view.html',tables=[df.to_html()],heading = name, output=query_list)

@app.route('/data/mf/<name>') 
def data1(name):
    # df = pd.read_csv(r'C:\Users\tanmo\Desktop\flaskProject\webPage\Output\stock_15032022.csv')
    dbx = dropbox.Dropbox("NVwGrPvFLxgAAAAAAAAAAVUBiyewqJ5KTDlXkSBRNBBsH2-aZ9iKQvRkP1bIDy_G")
    now = datetime.now()
    dropbox_path= "/results/" + str(name)
    result = dbx.files_get_temporary_link(dropbox_path)
    print(result.link)


    df = pd.read_csv(result.link, encoding= 'unicode_escape')
    return df.to_html()

@app.route('/sector')
def sector():
    now = datetime.now()
    file1 = str(now.strftime("%d%m%Y"))

    filename = 'Output/' + file1 + '.csv'
    for i in ticker:
        try:
            tik = i + '.NS'
            data = yf.Ticker(tik)
            print(i,data.info['sector'])
            with open(filename, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i, data.info['sector']])
        except:
            continue
    dropbox_access_token= "NVwGrPvFLxgAAAAAAAAAAVUBiyewqJ5KTDlXkSBRNBBsH2-aZ9iKQvRkP1bIDy_G"    #Enter your own access token
    dropbox_path= "/output/" + file1 + '.csv'
    computer_path= filename
    
    client = dropbox.Dropbox(dropbox_access_token)
    print("[SUCCESS] dropbox account linked")
    client.files_delete(dropbox_path)
    client.files_upload(open(computer_path, "rb").read(), dropbox_path)
    print("[UPLOADED] {}".format(computer_path))
    txt ="Unloaded in Dropbox Please Check"
    bot_token = '5041715929:AAFcraPI9-8jZR0bLkquRDNUXg96tEUKje4'
    bot_chatID = '1259144189'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id='+ bot_chatID + '&parse_mode=MarkdownV2&text=' + txt
    response = requests.get(send_text)
    print(response.json())

@app.route('/custom/analysis/<name>/<period>/<interval>') 
def analysis(name,period,interval):
    query_list = 'https://indianstockscanner-pre.herokuapp.com/custom/analysis/' + str(name) + '/'+ str(period) + '/' + str(interval) +'/csv'
    nameNS = name + '.NS'
    df = yf.download(tickers=nameNS, period=period, interval=interval)
    df[interval] = df['Close'].pct_change()*100
    df = df[df['Open'].notna()]
    #return df.to_html()
    return render_template('view.html',tables=[df.to_html()],heading = nameNS, output=query_list)

@app.route('/custom/analysis/<name>/<period>/<interval>/csv') 
def csv(name,period,interval):
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    nameNS = name + '.NS'
    df = yf.download(tickers=nameNS, period=period, interval=interval)
    df[interval] = df['Close'].pct_change()*100
    df = df[df['Open'].notna()]
    df.to_csv(name + ".csv")
    #return df.to_html()
    filename = str(d4) + "_" +name + "_" + str(period) + ".csv"
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=" + str(filename)
    resp.headers["Content-Type"] = "text/csv"
    return resp

# TWITTER SEARCH FUNCTIONALITY
@app.route('/tweet/<id>/<count>') 
def tweet(id,count):
    query_list = 'https://indianstockscanner-pre.herokuapp.com/tweet/' + str(id) + '/'+ str(count) + '/csv'
    query = "(from:"+str(id)+")"
    tweets = []
    limit = int(count)

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            link = tweet.content.split('https://')
            print(len(link))
            if len(link) > 1:
                link1 = link[1]
            else:
                link1 = ''
            tweets.append([tweet.date, tweet.username, tweet.content,link1])
            
    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet','Link'])
    return render_template('view.html',tables=[df.to_html()],heading = id, output=query_list)

@app.route('/tweet/<id>/<count>/csv') 
def tweetcsv(id,count):
    query = "(from:"+str(id)+")"
    tweets = []
    limit = int(count)

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limit:
            break
        else:
            link = tweet.content.split('https://')
            print(len(link))
            if len(link) > 1:
                link1 = link[1]
            else:
                link1 = ''
            tweets.append([tweet.date, tweet.username, tweet.content,link1])
            
    df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet','Link'])
    df.to_csv(id + ".csv")
    filename = str(id) + "_" + str(count) + ".csv"
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=" + str(filename)
    resp.headers["Content-Type"] = "text/csv"
    return resp


@app.route('/twittersearch', methods =["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["id"]
        count = request.form["cnt"]
        return redirect(url_for("tweet", id=user, count = count))
    else:
	    return render_template("twittersearch.html")

@app.route('/stockhistory', methods =["GET", "POST"])
def stockhistory():
    if request.method == "POST":
        ticker = request.form["ticker"]
        period = request.form["period"]
        interval = request.form["interval"]
        return redirect(url_for("analysis", name=ticker, period = period, interval=interval))
    else:
	    return render_template("stockhistorysearch.html")

# STOCK INFO FUNCTIONALITY
@app.route('/info/<stock>') 
def info(stock):
    query_list = 'https://indianstockscanner-pre.herokuapp.com/info/' + str(stock) + '/csv'
    tik = stock + '.NS'
    df = yf.Ticker(tik)
    temp = pd.DataFrame.from_dict(df.info, orient="index")
    temp.reset_index(inplace=True)
    temp.columns = ["Attribute", "Recent"]
    return render_template('view.html',tables=[temp.to_html()],heading = stock, output=query_list)

@app.route('/stockinfo', methods =["GET", "POST"])
def stockinfo():
    if request.method == "POST":
        ticker = request.form["ticker"]
        return redirect(url_for("info", stock=ticker))
    else:
	    return render_template("stockinfo.html")

@app.route('/info/<stock>/csv') 
def stockinfocsv(stock):
    tik = stock + '.NS'
    df = yf.Ticker(tik)
    temp = pd.DataFrame.from_dict(df.info, orient="index")
    temp.reset_index(inplace=True)
    temp.columns = ["Attribute", "Recent"]
    temp.to_csv(stock + ".csv")
    filename = str(stock) + ".csv"
    resp = make_response(temp.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=" + str(filename)
    resp.headers["Content-Type"] = "text/csv"
    return resp

# API Integration
@app.route('/api/custom/analysis/<name>/<period>/<interval>') 
def analysisapi(name,period,interval):
    query_list = 'https://indianstockscanner-pre.herokuapp.com/custom/analysis/' + str(name) + '/'+ str(period) + '/' + str(interval) +'/csv'
    nameNS = name + '.NS'
    df = yf.download(tickers=nameNS, period=period, interval=interval)
    df[interval] = df['Close'].pct_change()*100
    df = df[df['Open'].notna()]
    df.reset_index(level=0, inplace=True)
    df['index']=df['index'].astype(str)
    df = df.rename({'index': 'Date'}, axis=1)
    return Response(df.to_json(), mimetype='application/json')
    # return df.to_html()

#MMI
@app.route('/mmi') # https://indianstockscanner-pre.herokuapp.com/mmi
def mmi():
    URL = 'https://www.tickertape.in/market-mood-index'
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                'Accept-Language': 'en-US, en;q=0.5'})
  
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    mmi = dom.xpath('//*[@id="app-container"]/div/div[1]/div[1]/div/div[2]/span')[0].text
    day = dom.xpath('//*[@id="app-container"]/div/div[1]/div[1]/div/div[2]/p/text()[2]')[0]
    return render_template("MMI.html",mmi_page = mmi,last_updated = day)   
    


    
#Google Trends API Integration
#Gold Data
#pyspark stock compare report
#TwitterTrends with Volume
#BllombergNews,
#twitter tweets api integration
#News api integration
#Shortening lines using single function different action


if __name__ == "__main__":
    app.run(debug=True, port=10000)

# Deployment to Heroku Instructions (Heroku Git)
# Sign up for a free heroku account if you havent already done so
# Create app ie. myapp #name of app
# Type heroku login --> This will take you to a web based login page
# cd to your directory on your local drive
# Type 'git init'
# Type 'heroku git:remote -a myapp'
# Type 'git add .'
# Type ' git commit -am "version 1"'
# Type 'git push heroku master'
# Now you need to allocate a dyno to do the work. Type 'heroku ps:scale worker=1'
# If you want to check the logs to make sure its working type 'heroku logs --tail'
# Now your code will continue to run until you stop the dyno. To stop it scale it down using the command 'heroku ps:scale worker=0'
# heroku run bash 
