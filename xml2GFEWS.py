import ast
from collections import Counter
from sqlite3 import dbapi2 as sqlite
from xml.etree.ElementTree import iterparse
conn = sqlite.connect("fews.db")
cur=conn.cursor()

def elementtreetest():
	# I think I found a bug in elementtree which is demonstrated here. When:
	#	1. a tagname has exactly 13 characters.
	#	2. tags ident with exactly 2 spaces (in stead of tab for instance)
	# Then: For every 800-th repeated tag the value is ignored and set to ''.
	# Easy to avoid by strip trailing whitespace before. 
	bron='testing.xml'
	f1 = open ('%s'%(bron),'w') 
	f1.write ('<filters version="1.1">\n')
	for i in range(1,800):
		f1.write('  <%s>myValue</%s>\n'%('x'*13,'x'*13))
	f1.write('</filters>\n')
	f1.close()
	for (event, node) in iterparse(bron, ['start', 'end', 'start-ns', 'end-ns']):
		print "%s:\t%s"%(node.tag,node.text)
def striptrailing(bron):
	str1=''
	f1 = open ('%s'%(bron),'r')
	for line in f1:
		str1=str1+line.lstrip()
	f1.close()
	f2 = open ('%s'%(bron),'w')
	f2.write(str1)

def xml2sqlite(bron):
	cur=conn.cursor()
	cur.execute("drop table if exists elems")
	cur.execute("drop table if exists attrib")
	cur.execute("Create table elems (id integer,id_parent integer,tag varchar(100),text varchar(100), attrib text)")
	cur.execute("Create table attrib (id integer,id_elem integer,name varchar(100),value varchar(100))")
	niveau=0;num_0=0;eventvorig='init';attrib=0;attribvorig=0;
	for (event, node) in iterparse(bron, ['start', 'end', 'start-ns', 'end-ns']):
		if event=='end':
			niveau=niveau-1
		if event=='start':
			exec "numvorig_%s=num_%s"%(niveau,niveau)
			exec "elemvorig=niveau*10000000+numvorig_%s"%(niveau)
			niveau=niveau+1
			exec "if 'num_%s' not in locals(): num_%s=0"%(niveau,niveau)
			exec "num_%s=num_%s+1"%(niveau,niveau)
			exec "elem=niveau*10000000+num_%s"%(niveau)
			tag=node.tag
			if node.text:
				text=node.text.rstrip()
			else: text=''
			if node.keys():
				dict1={}
				for name in node.keys(): 
					attribvorig=attrib;attrib=attrib+1
					value=node.attrib.get(name)
					cur.execute("insert into attrib values ('%s','%s','%s','%s')"%(attrib,elem,name,value))
					dict1[name]=value
				attrib2=str(dict1)
			else:
				attrib2=''
			cur.execute("insert into elems values ('%s','%s','%s','%s',\"%s\")"%(elem,elemvorig,tag,text,attrib2))
		eventvorig=event

def mkdefaultsdict(tsssname):
	if (tsssname=='Default'):
		qrsub2=""
	elif (tsssname=='None'):
		qrsub2="and id_parent in (select elems.id from elems where elems.tag<>'timeSeriesSets')"
	else:
		qrsub2="""and id_parent in (\
select elems.id from elems,attrib where elems.id=attrib.id_elem \
and elems.tag='timeSeriesSets' and attrib.name='id' and attrib.value='%s')"""%(tsssname)
	qrsub="select id from elems where tag='timeSeriesSet' %s"%(qrsub2)
	qr0="""select distinct tag from elems where id_parent in (%s)"""%(qrsub)

	deflist={}
	cur=conn.cursor()
	cur.execute(qr0)
	for l in cur.fetchall():
		qr3="select id,text from elems where tag='%s' and id_parent in (%s) and id not in (select id_elem from attrib)"%(l[0],qrsub)
		cur.execute(qr3)	
		d={}
		j=cur.fetchall()
		if (len(j)>0):
			for elem in j:
				exec "d[%s]='%s'"%(elem[0],elem[1])
			e=Counter(d.values())
			maxe=max(e.values())
			sume=sum(e.values())
			if ((int(maxe)*100/int(sume)>50) and (maxe>1)): # at least 1 and at least 50% of total (but you can change this)
				attribdefault = [key for key, value in e.iteritems() if value == maxe][0]
			else: attribdefault = 'NonDefault'
			deflist[l[0]]=attribdefault 
		qr3="select id,text from elems where tag='%s' and id_parent in (%s) and id in (select id_elem from attrib)"%(l[0],qrsub)
		cur.execute(qr3)	
		d={}
		m=cur.fetchall()
		if (len(m)>0):
			for elem in m:
				h=elem[0]
				qr2="select name,value from attrib where id_elem=%s"%(h)
				cur.execute(qr2)
				b=cur.fetchall()
				if (len(b)>0):
					c={}
					for j in b:
						exec "c['%s']='%s'"%(j[0],j[1])
				exec "d[%s]=str(%s)"%(elem[0],c)
			e=Counter(d.values())
			maxe=max(e.values())
			sume=sum(e.values())
			if ((int(maxe)*100/int(sume)>50) and (maxe>1)): # at least 1 and at least 50% of total (but you can change this)
				u = [key for key, value in e.iteritems() if value == maxe][0]
			else:
				u = "'NonDefault'"
			attribdefault= ast.literal_eval(u)
			deflist[l[0]]=attribdefault 
	return deflist

def writeregulartimeSeriesSets(tsss):
	str1=''
	m=mkdefaultsdict(tsss)
	cur.execute("""
select id from elems where tag='timeSeriesSets' and id in (
select id_elem from attrib where name='id' and value='%s')
"""%(tsss))
	for h in cur.fetchall():
		cur.execute("select id,id_parent,tag,text,attrib from elems where tag='timeSeriesSet' and id_parent=%s"%(h[0]))
		tab0='\t'*(int(str(h[0])[0])-1)
		str1=str1+"%stimeSeriesSets(id:'%s') {\n"%(tab0,tsss)
		for i in cur.fetchall():
			tabs='\t'*(int(str(i[0])[0])-1)
			if (m<>mdef):
				str1=str1+"%s%s.tss_%s(\n"%(tabs,helpfilenm.replace('.groovy',''),tsss)
			else:
				str1=str1+"%s%s.tss_default(\n"%(tabs,helpfilenm.replace('.groovy',''))
			cur.execute("select id,id_parent,tag,text,attrib from elems where id_parent=%s"%(i[0]))
			for j in cur.fetchall():
				tabs2='\t'*(int(str(j[0])[0])-1)
				m2=m[j[2]]
				if (j[4]==''):
					attrib=j[3]
					str2="%s%s:'%s',\n"%(tabs2,j[2],j[3])
				else:
					attrib=j[4]
					str2="%s%s:%s,\n"%(tabs2,j[2],j[4].replace("{","[").replace("}","]"))
				if (attrib<>str(m2)):
					str1=str1+str2
			str1=str1+"%sdelegate\n"%(tabs2)
			str1=str1+"%s)\n"%(tabs)
		str1=str1+"%s}\n"%(tab0)
		return str1

def writeregulartimeSeriesSet(elem):
	cur.execute("select id,id_parent,tag,text,attrib from elems where id=%s"%(elem))
	for i in cur.fetchall():
		tabs='\t'*(int(str(i[0])[0])-1)
		if (mnone<>mdef):
			str1="%s%s.tss_None(\n"%(tabs,helpfilenm.replace('.groovy',''))
		else:
			str1="%s%s.tss_default(\n"%(tabs,helpfilenm.replace('.groovy',''))
		elemvorig=i[1]
		cur.execute("select id,id_parent,tag,text,attrib from elems where id_parent=%s"%(elem))
		for j in cur.fetchall():
			m2=mnone[j[2]]
			tabs2='\t'*(int(str(j[0])[0])-1)
			if(j[4]==''):
				attrib=j[3]
				str2="%s%s:'%s',\n"%(tabs2,j[2],j[3])
			else:
				attrib=j[4]
				str2="%s%s:%s,\n"%(tabs2,j[2],j[4].replace("{","[").replace("}","]"))
			if(attrib<>str(m2)):
				str1=str1+str2
		str1=str1+tabs2+"delegate\n"
		str1=str1+tabs+")\n"
		return str1
		
def writeregulargroovy(elem):
	if (elem==0):
		cur.execute("select min(id) from elems")
		for i in cur.fetchall():
			elem=i
	cur.execute("select id,id_parent,tag,text,attrib from elems where id=%s"%(elem))
	for i in cur.fetchall():
		tabs='\t'*(int(str(i[0])[0])-1)
		elemvorig=i[1]
		tag=i[2]
		text=i[3]
		attrib=i[4]
		if (tag not in ['timeSeriesSets','timeSeriesSet']):
			cur.execute("select id,id_parent,text,attrib from elems where id_parent=%s"%(elem))
			j2=cur.fetchall()	
			if (attrib==''):
				if (len(j2)>0):
					f1.write("%s%s('%s') {\n"%(tabs,tag,text))
				else:
					f1.write("%s%s('%s')\n"%(tabs,tag,text))
			else:
				if (len(j2)>0):
					f1.write("%s%s(%s) {\n"%(tabs,tag,attrib.replace('{','').replace('}','')))
				else:
					f1.write("%s%s(%s)\n"%(tabs,tag,attrib.replace('{','').replace('}','')))
			for j in j2:
				writeregulargroovy(j[0])
			if (len(j2)>0):
				f1.write("%s%s\n"%(tabs,'}'))
		if (tag=='timeSeriesSet'):
			cur.execute("select tag from elems where id=%s"%(elemvorig))
			for j in cur.fetchall():
				if (tag<>'timeSeriesSets'):
					f1.write(writeregulartimeSeriesSet(elem))
		if (tag=='timeSeriesSets'):
			cur.execute("select value from attrib where id_elem=%s and name='id'"%(elem))
			for j in cur.fetchall():
				f1.write(writeregulartimeSeriesSets(j[0]))
				
def writehelpergroovy():
	f2.write("static def tss_default(Map map,d) {\n")
	f2.write("\tdef defaults= [\n")
	# The general TSS defaults
	m=mkdefaultsdict('Default')
	tel=0
	for i in m:
		if (tel==0):
			str3="\t\t'%s':'%s'\n"%(i,m[i])
		else:
			str3="\t\t,'%s':'%s'\n"%(i,m[i])
		tel=tel+1
		f2.write(str3.replace("'{","[").replace("}'","]"))
	f2.write("\t]\n")
	f2.write("\tdef params = defaults + map\n")
	str1='\td.timeSeriesSet() { ['
	tel=0
	for i in m:
		if (tel==0):
			str1=str1+"'%s'"%(i)
		else:
			str1=str1+",'%s'"%(i)
		tel=tel+1

	str1=str1+"].each { k ->\n"
	f2.write(str1)
	f2.write("\t\t\"$k\"(params[k])\n")
	f2.write("\t\t}\n")
	f2.write("\t}\n")
	f2.write("}\n\n")
	# The TSSs specific TSS defaults
	cur.execute("""
select distinct value from attrib where name='id' and id_elem in (
select id from elems where tag='timeSeriesSets')
""")
	i2=cur.fetchall()
	i2.append(('None',)) # Voeg een helper toe voor alle tss zonder tsss
	for i in i2:
		str2="\tdef %s_params = [\n"%(i[0])
		m2=mkdefaultsdict("%s"%(i[0]))
		tel=0
		for j in m2:
			#if(m2[j]<>m[j]):
			if(str(m2[j])<>str(m[j])):
				if (tel==0):
					str2=str2+"\t\t'%s':'%s'\n"%(j,m2[j])
				else:
					str2=str2+"\t\t,'%s':'%s'\n"%(j,m2[j])
				tel=tel+1
		if (str2<>"\tdef %s_params = [\n"%(i[0])): # No specific TSS defaults if they are all the same as the general defaults
			f2.write("static def tss_%s(Map map,d) {\n"%(i[0]))
			str2=str2.replace("'{","[").replace("}'","]")
			str2=str2+'\t]\n'
			f2.write(str2)
			f2.write("\ttss_default(%s_params + map,d)\n"%(i[0]))
			f2.write("}\n\n")

# PARAMETERS
####################################################################################################### 
inputfilenm='testinput.xml'
regfilenm='testoutput.groovy'
helpfilenm='__Helpers.groovy'
# INITIALS
####################################################################################################### 
f1 = open ('%s'%(regfilenm),'w') 
f2 = open ('%s'%(helpfilenm),'w') 
f1.write("import static GroovyFewsHelpers.*\n")
f1.write("import groovy.xml.StreamingMarkupBuilder\n")
f1.write("import groovy.xml.XmlUtil\n")
f1.write("def outputFile = new File(args[0])\n")
f1.write("def writer = outputFile.newWriter()\n")
f1.write("def xmlBuilder = new StreamingMarkupBuilder()\n")
f1.write("xmlBuilder.useDoubleQuotes=true\n")
f1.write("def builderResult = xmlBuilder.bind {\n")
# ACTIONS
####################################################################################################### 
#elementtreetest()			   # Illustrates a bug i elementtree
striptrailing(inputfilenm)	   	   # Because of a bug in elementree remove trailing whitespace
xml2sqlite(inputfilenm) 		   # Convert fews xml into sqlite db
mdef=mkdefaultsdict('Default') 		   # Create general defaults on all TSS
mnone=mkdefaultsdict('None') 		   # Create specific defaults on TSS without a TSSS
#m=mkdefaultsdict('set1') 		   # Create specific defaults on TSS under a specific TSSS
####################################################################################################### 
# writeregulartimeSeriesSets('set1')       # write timeSeriesSets's (called by writeregulargroovy)
# writeregulartimeSeriesSet(30000646)      # write timeSeriesSet's (called by writeregulargroovy)
writeregulargroovy(0) 			   # write regular groovy file
writehelpergroovy()			   # write helper groovy file
# FINISHING
####################################################################################################### 
f1.write("}\n")
f1.write("writer << XmlUtil.serialize(builderResult)\n")
f1.write("writer.close()\n")
conn.commit()
conn.close()
