# -*- coding: UTF-8 -*- 


"""
Created on 12 avr. 2010

@author: Assem Chelli
@contact: assem.ch[at]gmail.com

"""
CONFIGPATH="./"
INDEXPATH="./indexes/"


from configobj import ConfigObj
from PyQt4 import  QtGui,QtCore
from PyQt4.QtCore import QRect




from mainform import Ui_MainWindow
import sys


from alfanous.main import * #alfanous.

import gettext;
gettext.bindtextdomain("alfanousQT", "./locale");
gettext.textdomain("alfanousQT");
_=gettext.gettext
n_ = gettext.ngettext




QSE=QuranicSearchEngine(INDEXPATH+"main/")
TSE=TraductionSearchEngine(INDEXPATH+"extend/")
PERPAGE=10
CPTZ=0


from re import compile
kword = compile(u"[^,،]+")
keywords = lambda phrase: kword.findall(phrase)


def Gword_tamdid(aya):
    """ add a tamdid to lafdh aljalala to eliminate the double vocalization """
    return aya.replace(u"لَّه", u"لَّـه").replace(u"لَّه", u"لَّـه")

langs={'el': 'Greek', 'eo': 'Esperanto', 'en': 'English', 'vi': 'Vietnamese', 'ca': 'Catalan', 'it': 'Italian', 'lb': 'Luxembourgish', 'eu': 'Basque', 'ar': 'Arabic', 'bg': 'Bulgarian', 'cs': 'Czech', 'et': 'Estonian', 'gl': 'Galician', 'id': 'Indonesian', 'ru': 'Russian', 'nl': 'Dutch', 'pt': 'Portuguese', 'no': 'Norwegian', 'tr': 'Turkish', 'lv': 'Latvian', 'lt': 'Lithuanian', 'th': 'Thai', 'es_ES': 'Spanish', 'ro': 'Romanian', 'en_GB': 'British English', 'fr': 'French', 'hy': 'Armenian', 'uk': 'Ukrainian', 'pt_BR': 'Brazilian', 'hr': 'Croatian', 'de': 'German', 'da': 'Danish', 'fa': 'Persian', 'bs': 'Bosnian', 'fi': 'Finnish', 'hu': 'Hungarian', 'ja': 'Japanese', 'he': 'Hebrew', 'ka': 'Georgian', 'zh_CN': 'Chinese', 'kk': 'Kazakh', 'sr': 'Serbian', 'sq': 'Albanian', 'ko': 'Korean', 'sv': 'Swedish', 'mk': 'Macedonian', 'sk': 'Slovak', 'pl': 'Polish', 'ms': 'Malay', 'sl': 'Slovenian'}




sura_reallist=[item for item in QSE.list_values("sura") if item]

relations=["","",u"|",u"+",u"-"]
relate=lambda query,filter,index:"( "+unicode(query)+" ) "+relations[index]+" ( "+filter+" ) " if  index>1 else filter if index==1 else unicode(query)+" "+filter


class QUI(Ui_MainWindow):
    """ the Quranic UI"""
    def __init__(self):
        self.last_results=None
        self.last_terms=None
        self.history=[]
        
        
    def exit(self):
        self.save_config()
        sys.exit()
        
       
       
        
    def load_config(self):
        """load configuration"""
        config=ConfigObj(CONFIGPATH+"config.ini")
        boolean=lambda s:True if s=="True" else False
        self.o_query.clear()
        self.o_query.addItems(map(lambda x:x.decode("utf-8"),config["history"]) if config.has_key("history") else [u"الحمد لله"])
        self.o_limit.setValue(int(config["options"]["limit"]) if config.has_key("options") else 100)
        self.o_perpage.setValue(int(config["options"]["perpage"]) if config.has_key("options") else 10)
       
        self.o_sortedbyscore.setChecked(boolean(config["sorting"]["sortedbyscore"]) if config.has_key("sorting") else True)
        self.o_sortedbymushaf.setChecked(boolean(config["sorting"]["sortedbymushaf"]) if config.has_key("sorting") else False)
        self.o_sortedbytanzil.setChecked(boolean(config["sorting"]["sortedbytanzil"]) if config.has_key("sorting") else False)
        self.o_sortedbysubject.setChecked(boolean(config["sorting"]["sortedbysubject"]) if config.has_key("sorting") else False)
        self.o_sortedbyfield.setChecked(boolean(config["sorting"]["sortedbyfield"]) if config.has_key("sorting") else False)
        
        self.o_field.setCurrentIndex(int(config["sorting"]["field"]) if config.has_key("sorting") else 0)
        self.o_reverse.setChecked(boolean(config["sorting"]["reverse"])if config.has_key("sorting") else False)  
              
        self.o_prev.setChecked(boolean(config["extend"]["prev"]) if config.has_key("extend") else False)
        self.o_suiv.setChecked(boolean(config["extend"]["suiv"])if config.has_key("extend") else False)
        
        self.o_traduction.setCurrentIndex(int(config["extend"]["traduction"]) if config.has_key("extend") else 0)
        self.o_recitation.setCurrentIndex(int(config["extend"]["recitation"]) if config.has_key("extend") else 0)
        
        self.o_script_uthmani.setChecked(boolean(config["script"]["uthmani"]) if config.has_key("script") else False)
        self.o_script_standard.setChecked(boolean(config["script"]["standard"]) if config.has_key("script") else True)
          
        self.w_features.setHidden(not boolean(config["widgets"]["features"]) if config.has_key("widgets") else False)
        self.w_options.setHidden(not boolean(config["widgets"]["options"]) if config.has_key("widgets") else True)
        self.m_options.setChecked (boolean(config["widgets"]["options"]) if config.has_key("widgets") else False)
        self.m_features.setChecked (boolean(config["widgets"]["features"]) if config.has_key("widgets") else True)
        
 
    def save_config(self):
        """save configuration """
        config=ConfigObj(CONFIGPATH+"config.ini")
        config["history"]=map(lambda x:x,config["history"]) if config.has_key("history") else ["الحمد لله"]
        
        config["options"]={}
        config["options"]["limit"]=self.o_limit.value()
        config["options"]["perpage"]=self.o_perpage.value()
        config["options"]["highlight"]=self.o_highlight.isChecked()
        
        config["sorting"]={}
        config["sorting"]["sortedbyscore"]=self.o_sortedbyscore.isChecked()
        config["sorting"]["sortedbymushaf"]=self.o_sortedbymushaf.isChecked()
        config["sorting"]["sortedbytanzil"]=self.o_sortedbytanzil.isChecked()
        config["sorting"]["sortedbysubject"]=self.o_sortedbysubject.isChecked()
        config["sorting"]["sortedbyfield"]=self.o_sortedbyfield.isChecked()
        config["sorting"]["field"]=self.o_field.currentIndex()
        config["sorting"]["reverse"]=self.o_reverse.isChecked()
        
        
        config["extend"]={}
        config["extend"]["prev"]=self.o_prev.isChecked()
        config["extend"]["suiv"]=self.o_suiv.isChecked()
        config["extend"]["traduction"]=self.o_traduction.currentIndex()
        config["extend"]["recitation"]=self.o_recitation.currentIndex()
        
        config["script"]={}
        config["script"]["uthmani"]=self.o_script_uthmani.isChecked()
        config["script"]["standard"]=self.o_script_standard.isChecked()
        
        config["widgets"]={}
        config["widgets"]["features"]=not self.w_features.isHidden()
        config["widgets"]["options"]=not self.w_options.isHidden() 
        config.write()


    def setupUi(self, MainWindow):
        super(QUI, self).setupUi(MainWindow)
        QtCore.QObject.connect(self.o_search, QtCore.SIGNAL("clicked()"), self.search_all)
        QtCore.QObject.connect(self.o_page, QtCore.SIGNAL("valueChanged(int)"), self.changepage)
        QtCore.QObject.connect(self.o_chapter, QtCore.SIGNAL("activated(QString)"), self.topics)
        QtCore.QObject.connect(self.o_topic, QtCore.SIGNAL("activated(QString)"), self.subtopics)
        QtCore.QObject.connect(self.o_sajdah_exist, QtCore.SIGNAL("activated(int)"), self.sajda_enable)
        QtCore.QObject.connect(self.o_struct_as, QtCore.SIGNAL("activated(QString)"), self.setstructborn)
        QtCore.QObject.connect(self.o_perpage, QtCore.SIGNAL("valueChanged(int)"), self.changePERPAGE)
        QtCore.QObject.connect(self.o_struct_from, QtCore.SIGNAL("valueChanged(int)"), self.struct_to_min)
        QtCore.QObject.connect(self.o_stat_from, QtCore.SIGNAL("valueChanged(int)"), self.stat_to_min)
        QtCore.QObject.connect(self.tb_exit,QtCore.SIGNAL("clicked()"),self.exit)
        QtCore.QObject.connect(self.tb_help,QtCore.SIGNAL("clicked()"), self.help)
        QtCore.QObject.connect(self.tb_about,QtCore.SIGNAL("clicked()"), self.about)
        QtCore.QObject.connect(self.tb_save,QtCore.SIGNAL("clicked()"), self.save_results)
        QtCore.QObject.connect(self.tb_print,QtCore.SIGNAL("clicked()"), self.print_results)

        QtCore.QObject.connect(self.o_add2query_advanced, QtCore.SIGNAL("clicked()"), self.add2query_advanced)
        QtCore.QObject.connect(self.o_add2query_struct, QtCore.SIGNAL("clicked()"), self.add2query_struct)
        QtCore.QObject.connect(self.o_add2query_stat, QtCore.SIGNAL("clicked()"), self.add2query_stat)
        QtCore.QObject.connect(self.o_add2query_subject, QtCore.SIGNAL("clicked()"), self.add2query_subject)
        QtCore.QObject.connect(self.o_add2query_word, QtCore.SIGNAL("clicked()"), self.add2query_word)
        QtCore.QObject.connect(self.o_add2query_misc, QtCore.SIGNAL("clicked()"), self.add2query_misc)

        self.o_chapter.addItems([item for item in QSE.list_values("chapter") if item])
        self.o_sura_name.addItems([keywords(item)[0] for item in QSE.list_values("sura") if item])
        self.o_field.addItems(ara2eng_names.keys())
        self.o_traduction.addItems(self.traductions_dict(static=True).values())
        
        self.load_config()


        

        
    def search_all(self):
        """ 
        The main search function 
        """

        #inputs
        query=self.o_query.currentText()
        self.history.insert(0,query)
        self.o_query.clear()
        self.o_query.addItems(self.history)
        self.o_query.setCurrentIndex(0)
        bymushaf=self.o_sortedbymushaf.isChecked()
        bytanzil=self.o_sortedbytanzil.isChecked()
        byscore=self.o_sortedbyscore.isChecked()
        bysubject=self.o_sortedbysubject.isChecked()
        byfield=self.o_sortedbyfield.isChecked()
        field=unicode(self.o_field.currentText())
        
        sortedby="score" if byscore  else "mushaf" if bymushaf else "tanzil" if bytanzil else "subject" if bysubject else ara2eng_names[field]
        reverse_sort=self.o_reverse.isChecked()
        limit=self.o_limit.value()
        highlight=self.o_highlight.isChecked()
        

        html=self.suggest(query)
        #search
        results, terms = QSE.search_all(unicode(query),limit=limit, sortedby=sortedby,reverse=reverse_sort)
        
        #print terms
        wordshtml=""
        matches=0
        docs=0
        cpt=1;
        for term in terms :
            if term[0]=="aya":
                
                if term[2]:                
                    matches+=term[2]
                    docs+=term[3]
                    wordshtml+=u'<p dir="%s" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; color:#00aa00;">%d .  </span><span style=" font-size:14pt; color:#005800;">%s : </span><span style=" font-size:14pt;"> %s </span><span style=" font-size:14pt; color:#005500;">%d </span> %s <span style=" font-size:14pt;"> %s  </span><span style=" font-size:14pt; color:#005500;">%d</span><span style=" font-size:14pt;"> %s</span>.' %  (_(u"ltr"),cpt,term[1],_(u"reported"),term[2],n_(u"time",u"times",term[2]),_(u"in"),term[3],n_(u"aya",u"ayas",term[3]))
                    cpt+=1
                wordshtml+=u"</p>"
        if cpt-1:
            html+=u'<p dir="%s" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:16pt; font-weight:600; color:#ff0000;">%s </span><span style=" font-size:14pt; font-weight:600; color:#6a0000;"> </span><span style=" font-size:16pt; color:#6a0000;">( </span><span style=" font-size:16pt; color:#ff0000;">%d</span><span style=" font-size:16pt; color:#6a0000;"> %s %s </span><span style=" font-size:16pt; color:#ff0000;">%d</span><span style=" font-size:16pt; color:#6a0000;"> %s  </span><span style=" font-size:16pt; color:#6a0000;"> )</span><span style=" font-size:18pt; font-weight:600; color:#ff0000;"> : </span></p>' %  (_(u"ltr"),_(u"Words"),cpt-1,n_(u"word",u"words",cpt-1),_(u"reported"),matches,n_(u"time",u"times",matches))
            html+= wordshtml   
            html+=u"<br>"
            
        terms = [term[1] for term in list(terms)]
        if self.o_filter.isChecked() and self.last_results:
            results=QFilter(self.last_results,results)
            


        self.last_results=results
        self.last_terms=terms
        res=self.results(results,terms, sortedby=sortedby,page=1,highlight=highlight)
        #outputs
        self.o_time.display(res["time"])
        self.o_time_extend.display(res["extend_time"])
        self.o_resnum.display(res["resnum"])
        numpagereal=(res["resnum"]-1)/PERPAGE+1
        numpagelimit=(limit-1)/PERPAGE+1 
        numpage=numpagelimit if numpagelimit<numpagereal else numpagereal 
        
        self.o_numpage.display(numpage)
        self.o_page.setMaximum(numpage)
        self.o_page.setValue(1)
        
        html+=res["results"]
        self.o_results.setText(html)
        
        
        self.o_results.setText(html)       

        
        pass
    

    


    def results(self,results,terms, sortedby="score", recitation="Mishary Rashid Alafasy",page=1,highlight=True):
        """
        return the results
        @param fields : fields enabled to be shown
        @return : the results 
        """
        res=results
        #pagination
        page=int(page)
        startpage =(page-1)*PERPAGE
        endpage=(page)*PERPAGE
        end=endpage if endpage<len(res) else len(res)
        start=startpage if startpage<len(res) else -1
        reslist=[] if end==0 or start==-1 else list(res)[start:end]
        extend_runtime=0

        H=lambda X:QSE.highlight(X, terms,"html") if highlight and X else X if X else u"-----"
        N=lambda X:X if X else 0
        
        #+prev +succ
        prev=self.o_prev.isChecked()
        suiv=self.o_suiv.isChecked()
        
        if prev or suiv:
            adja_query=u"( 0"
            for r in reslist :
                if prev: adja_query+=" OR gid:"+unicode(r["gid"]-1)+u" "
                if suiv:adja_query+=" OR gid:"+unicode(r["gid"]+1)+u" "
            adja_query+=" )"
            adja_res=QSE.find_extended(adja_query, "gid")
            adja_ayas={0:{"aya_":u"----","uth_":u"----","sura":u"---","aya_id":0},6237:{"aya_":u"----","uth_":u"----","sura":u"---","aya_id":9999}}
            for adja in adja_res:
                adja_ayas[adja["gid"]]={"aya_":adja["aya_"],"uth_":adja["uth_"],"aya_id":adja["aya_id"],"sura":adja["sura"]}
            extend_runtime+=adja_res.runtime

        #traductions
        trad_index=self.o_traduction.currentIndex()
        if trad_index:
            trad_title=self.o_traduction.currentText()
            trad_id=None
            for k,v in self.traductions_dict(static=True).items():
                if v==trad_title:
                    trad_id=k
                    break
            trad_query=u"( 0"
            for r in reslist :
                trad_query+=" OR gid:"+unicode(r["gid"])+u" "
            trad_query+=" )"+u" AND id:"+unicode(trad_id)
            trad_res=TSE.find_extended(trad_query, "gid")
            trad_text={}
            for tr in trad_res:
                trad_text[tr["gid"]]=tr["text"]
            extend_runtime+=trad_res.runtime
                
            
        
        html=""
        if reslist:
            html+=u"<p  dir='%s' style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15pt; font-weight:600; color:#ff0000;\">%s (%d %s %d)</span></p>" % (_(u"ltr"),_(u"Results"),start+1,_(u"to"),end)
        
        
            
        cpt = startpage
        for r in reslist :
            cpt += 1
            html += u"<p %s style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'arial ,sans serif'; color:#0000ff; background-color:#ccffcc;\"> %s <span style=\" font-family:'arial ,sans serif'; font-weight:600; color:#0000ff;\"> <b>%d</b> </span><span style=\" font-family:'arial ,sans serif'; color:#0000ff;\">  - %s </span><span style=\" font-family:'arial ,sans serif'; font-weight:600; color:#0000ff;\"> <b>%d</b> </span><span style=\" font-family:'arial ,sans serif'; color:#0000ff;\"> %s </span><span style=\" font-family:'arial ,sans serif'; font-weight:600; color:#0000ff;\"> <b>%s</b> </span><span style=\" font-family:'arial ,sans serif'; color:#0000ff;\">(<span style=\" font-size:8pt; color:#404060;\">   %s: <b>%d</b>,%s : <b>%s</b> , %s :  <b>%d</b>, %s : <b>%d</b>, %s  :<b>%d</b>, %s :<b>%d</b>, %s :<b>%d</b>, %s :<b>%d</b></span>)</p>" %(_(u"dir='ltr'"),_(u"N°"),cpt,_(u"Aya n°"),r["aya_id"],_(u"of Sura "),H(keywords(r["sura"])[0]),_(u"n°"),r["sura_id"],_(u"revel_place"),H(r["sura_type"]),_(u"revel_order"),r["sura_order"],_(u"ayas"),r["s_a"],_(u"words"),N(r["s_w"]),_(u"names of Allaah"),N(r["s_g"]),_(u"letters"),N(r["s_l"]),_(u"ruku's"),N(r["s_r"]))
            html+="<br />"
            if prev:
                html += u"<p dir='rtl' align=\"center\" style=\"margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\"font-family:'ArabeyesQr';  font-size:10pt;font-weight:200; color:#bc947a;\">[ <span style=\"font-family:'me_quran';\"><b>%s</b></span>] - %s %d </span></p>" % (Gword_tamdid(adja_ayas[r["gid"]-1]["uth_"] if self.o_script_uthmani.isChecked() else adja_ayas[r["gid"]-1]["aya_"] ),keywords(adja_ayas[r["gid"]-1]["sura"])[0],adja_ayas[r["gid"]-1]["aya_id"])
            html += u" <p dir='rtl' align=\"center\" style=\"margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\"font-family:'ArabeyesQr';  font-size:18pt; font-weight:800; color:#6b462a;\">[ <span style=\"font-family:'me_quran';\"><b>%s</b></span>]  </span></p>" % Gword_tamdid(H(r["uth_"] if self.o_script_uthmani.isChecked() else r["aya_"] ) )
            if suiv:
                html += u"<p dir='rtl' align=\"center\" style=\"margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\"font-family:'ArabeyesQr'; font-size:10pt; font-weight:200; color:#bc947a;\">[ <span style=\"font-family:'me_quran';\"><b>%s</b></span>] - %s %d </span></p>" % (Gword_tamdid(adja_ayas[r["gid"]+1]["uth_"] if self.o_script_uthmani.isChecked() else adja_ayas[r["gid"]+1]["aya_"] ),keywords(adja_ayas[r["gid"]+1]["sura"])[0],adja_ayas[r["gid"]+1]["aya_id"])
            html+="<br />"
            if trad_index: 
                if trad_id: 
                    html += u'<p %s align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style="font-size:18pt; font-weight:600; color:#5500ff;">%s (%s):</span></p><p dir="ltr" align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">%s</span></p><br/>' % (_("dir='ltr'"),_(u"translation"),trad_title,trad_text[r["gid"]])
            html += u"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#808080;\">%s:   <b>%d</b> -(%s : <b>%d</b> , %s : <b>%d</b>) - %s :<b>%d</b> -  %s :<b>%s</b></span></p> " % (_(u"manzil"),r["manzil"],_(u"hizb"),r["hizb"],_(u"rubu'"),r["rub"],_(u"ruku'"),r["ruku"],_(u"page"),r["page"])       
            html += u"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#808080;\">%s : <b>%s</b> %s : <b>%s</b> %s : <b>%s</b> </span></p>" % (_(u"chapter"),H(r["chapter"]),_(u"topic"),H(r["topic"]),_(u"subtopic"),H(r["subtopic"]))        
            html += u"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#808080;\">%s : </span><span style=\" font-weight:600; color:#808080;\"> <b>%d</b> </span><span style=\" color:#808080;\"> - %s :  <b>%d</b>  </span><span style=\" color:#808080;\"> - %s :  <b>%d</b>  </span></p>" % (_(u"words"),N(r["a_w"]),_(u"letters"),N(r["a_l"]),_(u"names of Allaah"),N(r["a_g"]))
            if r["sajda"]==u"نعم": html+=u'<p align="center" %s style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#b88484;">%s  %s,%s %d</span></p>' % (_("dir='rtl'"),_(u"This aya contain a sajdah"),H(r["sajda_type"]),_(u"N°"),N(r["sajda_id"]))
            html += u"<hr />"
        
        return {"results":html,"time":res.runtime,"resnum":len(res),"extend_time":extend_runtime}
        
    @staticmethod
    def suggest(query):
        """ return lines of suggestions
        """
        try:
            items=QSE.suggest_all(unicode(query)).items()
            text=u""
            if len(items):
                text=u"<p  %s style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:15pt; font-weight:600; color:#ff0000;\">%s (%d)</span></p>" %(_("dir='ltr'"),_(u"Suggestions"),len(items))
                for key, value in items:
                        text +=u"<p  dir='rtl' style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#246b14;\">%s</span><span style=\" font-weight:600; color:#246f0d;\">:</span><span style=\" color:#000000;\">%s.</span></p>" % (unicode(key),u"،".join(value))
                        
               
        except Exception:
            text =""
            
        return text  
    @staticmethod  
    def traductions_dict(static=True):
        if static:
            return TDICT
        else:
            list1=[item for item in TSE.list_values("id") if item]
            list2=[]
            list3=[]
            for id in list1:
                list2.extend([item for item in TSE.list_values("lang",conditions=[("id",id)]) if item])
                list3.extend([item for item in TSE.list_values("author",conditions=[("id",id)]) if item])
            list5=map(lambda x: langs[x] if langs.has_key(x) else x,list2)
            D={}
            for i in range(len(list3)):
                D[list1[i]]=list3[i]+"-"+list5[i]
            return D

    
    def changepage(self,value):
        #inputs
        bymushaf=self.o_sortedbymushaf.isChecked()
        bytanzil=self.o_sortedbytanzil.isChecked()
        byscore=self.o_sortedbyscore.isChecked()
        bysubject=self.o_sortedbysubject.isChecked()
        byfield=self.o_sortedbyfield.isChecked()
        field=unicode(self.o_field.currentText())
        
        sortedby="score" if byscore  else "mushaf" if bymushaf else "tanzil" if bytanzil else "subject" if bysubject else ara2eng_names[field]
        
        page=value
        highlight=self.o_highlight.isChecked()
        #search
        res=self.results(self.last_results,self.last_terms, sortedby=sortedby,page=page,highlight=highlight)
  


        
        html=res["results"]
        self.o_results.setText(html)
    
    def topics(self,chapter):
        
      
        first=self.o_topic.itemText(0)
        list=[item for item in QSE.list_values("topic",conditions=[("chapter",unicode(chapter))]) if item]
        list.insert(0, first)
        self.o_topic.clear()
        self.o_topic.addItems(list)
        pass
    
    def subtopics(self,topic):
    
        first=self.o_subtopic.itemText(0)
        list=[item for item in QSE.list_values("subtopic",conditions=[("topic",unicode(topic)),]) if item]
        list.insert(0, first)
        self.o_subtopic.clear()
        self.o_subtopic.addItems(list)
        pass
    
    def changePERPAGE(self,perpage):
        global PERPAGE
        PERPAGE=perpage


    def add2query_advanced(self):
        """
        """
        filter=""
        
        text=unicode(self.o_feature_text.text())
        word_re=compile("[^ \n\t]+")
        words=word_re.findall(text)
        if text:
            if self.o_synonyms.isChecked():
                for word in words:filter+=" ~"+word
            elif self.o_antonyms.isChecked():
                for word in words:filter=" #"+word
            elif self.o_orthograph.isChecked():
                for word in words: filter=" %"+word
            elif self.o_vocalization.isChecked():
                filter=u" آية_:'"+text+"'"
            elif self.o_phrase.isChecked():
                filter=" \""+text+"\""
            elif self.o_partofword.isChecked():
                for word in words: filter=" *"+word+"*"
            elif self.o_allwords.isChecked():
                filter=u" + ".join(words)
            elif self.o_somewords.isChecked():
                filter=u" | ".join(words)
            elif self.o_nowords.isChecked():
                filter=u" - ".join(words)
            elif self.o_derivation_light.isChecked():
                for word in words:filter+=" >"+word
            elif self.o_derivation_deep.isChecked():
                for word in words:filter+=" >>"+word
            elif self.o_boost.isChecked():
                filter=" ("+text+")^2"    
            
        index=self.o_relation_advanced.currentIndex()
        newquery=relate(self.o_query.currentText(),filter,index)

        if text:
            self.o_query.setEditText(newquery)
    
    def add2query_struct(self):
        """
         """
        filter=""
        items_fields=[u"رقم_الآية",u"رقم",u"ركوع",u"رقم_السورة",u"صفحة",u"ربع",u"حزب",u"جزء",u"منزل"]
        
        index=self.o_struct_as.currentIndex()
        vfrom=self.o_struct_from.value()
        vto=self.o_struct_to.value()
        
        filter=u"  "+items_fields[index]+u":["+unicode(vfrom)+u" إلى  "+unicode(vto)+"]" 
        
        
        index=self.o_relation_struct.currentIndex()
        newquery=relate(self.o_query.currentText(),filter,index)
        
        self.o_query.setEditText(newquery)

    
    def add2query_subject(self):        
        """        """
        filter=""
        if self.o_chapter.currentIndex()!=0:
            filter+=u"  فصل:\""+unicode(self.o_chapter.currentText())+"\""
        
          
        if self.o_topic.currentIndex()>0:
            filter+=u" + فرع:\""+unicode(self.o_topic.currentText())+"\""

        
        if self.o_subtopic.currentIndex()>0:
            filter+=u" + باب:\""+unicode(self.o_subtopic.currentText())+"\"" 
        
        index=self.o_relation_subject.currentIndex()
        newquery=relate(self.o_query.currentText(),filter,index)
        self.o_query.setEditText(newquery)

    
    def add2query_stat(self):
        """
         """
        filter=""
        i=self.o_stat_num.currentIndex()
        j=self.o_stat_in.currentIndex()
        vfrom=self.o_stat_from.value()
        vto=self.o_stat_to.value()
        
        STATIN=["",u"آ",u"س"]
        STATNUM=["",u"ح",u"ك",u"ج",u"آ",u"ر"]
        if i*j!=0 and i/4+1<=j:
            filter+=u" "+STATNUM[i]+"_"+STATIN[j]+u":["+str(vfrom)+u" إلى "+str(vto)+u"]"
            
        index=self.o_relation_stat.currentIndex()
        newquery=relate(self.o_query.currentText(),filter,index)
        self.o_query.setEditText(newquery)
    
    def add2query_misc(self):
        """
         """
        filter=u""
        
        if self.o_sura_name.currentIndex()!=0:
            filter+=u"  سورة:\""+unicode(sura_reallist[self.o_sura_name.currentIndex()-1])+"\""
            
        sura_types=[u"",u"مدنية",u"مكية"]
        if self.o_tanzil.currentIndex()!=0:
            filter+=u"  نوع_السورة:"+unicode(sura_types[self.o_tanzil.currentIndex()])
        
        
        yes_no=["",u"لا",u"نعم"]
        sajdah_types=["",u"مستحبة",u"واجبة"]
        if self.o_sajdah_exist.currentIndex()!=0:
            if self.o_sajdah_type.currentIndex()==0:
                filter+=u"  سجدة:"+unicode(yes_no[self.o_sajdah_exist.currentIndex()])
            else: 
                filter+=u"  نوع_السجدة:"+unicode(sajdah_types[self.o_sajdah_type.currentIndex()])
                                              
        index=self.o_relation_misc.currentIndex()
        newquery=relate(self.o_query.currentText(),filter,index)
        if filter:self.o_query.setEditText(newquery)

        
    def add2query_word(self):
        filter=""
        root=unicode(self.o_word_root.text())
        
        type_values=[u"اسم",u"فعل",u"أداة"]
        type=type_values[self.o_word_type.currentIndex()]
        filter=u" {"+root+u"،"+type+u"}"
        
        index=self.o_relation_word.currentIndex()
        newquery=relate(self.o_query.currentText(),filter,index)
        if root:self.o_query.setEditText(newquery)
        
    def setstructborn(self):
        
        items_max=[286,6236,565,114,604,240,60,30,7]
        max=items_max[self.o_struct_as.currentIndex()]
        self.o_struct_from.setMaximum(max)
        self.o_struct_to.setMaximum(max)
    def struct_to_min(self,nb):
        self.o_struct_to.setMinimum(nb)
    
    def stat_to_min(self,nb):
        self.o_stat_to.setMinimum(nb)  
        
    def sajda_enable(self,index):
        if index==2:
            self.o_sajdah_type.setEnabled(True)
        else:
            self.o_sajdah_type.setDisabled(True)
            
    def save_results(self):
        """save as html file"""
        diag= QtGui.QFileDialog( )
        diag.setAcceptMode(diag.AcceptSave)
        diag.setFileMode(diag.AnyFile)
        diag.setFilter("*.html")
        filenames=["./results.html    "]
        if (diag.exec_()):
            filenames = diag.selectedFiles();
            
        path=unicode(filenames[0])
        file=open(path,"w")
        file.write(self.o_results.toHtml()+"<br><br>CopyRights(c)<a href='http://alfanous.sf.net/cms/'>Alfanous</a>  ")
        file.close()
        
    def print_results(self):
        printer = QtGui.QPrinter()
        printer.setCreator(self.o_results.toHtml())
        printer.setDocName(_(u"Results")+"-"+str(self.o_page.value()))
        printer.setPageSize(printer.A4)


        dialog = QtGui.QPrintDialog(printer, None)
        if dialog.exec_():
            pass
    
        painter = QtGui.QPainter(printer)
        
        painter.drawText(10,10,_("This is not a bug,Printing will be available in next releases insha'allah"))
        painter.setFont(QtGui.QFont("Arabeyesqr"))
        metrics = (painter.device().width(),painter.device().height())
        marginHeight = 6
        marginWidth =  8
        body = QRect(marginWidth, marginHeight,metrics[0] - 2 * marginWidth,metrics[1] - 2 * marginHeight)
        #painter.drawRect(body)
        i=0
        for line in self.o_results.toPlainText().split("\n"):
            i+=1 
            if "[" not in line:
                painter.drawText(10,30+10*i,line)
            

        painter.end()


           
        
            
    def about(self):
        html="""
        <style type="text/css">
          h1 { color : green }
          h2 { color : red }
          h3,b { color : blue}

        </style>
               
        """+_(u'''   
Alfanous is a Quranic search engine provides simple and advanced search services in the diverse information of the Holy Quran .


<ul>
<li> <b>  Mailinglist:</b> alfanous@googlegroup.com </li>
<li> <b>  website :</b> http://alfanous.sf.net/cms/ </li>
<li> <b>  Developer :</b> Assem.ch [at] gmail.com </li>

</ul>








</div>   


''')
        
        self.o_results.setText(html)
   
        
        


    
    
      
    
    
    def help(self):
        """       """
        html="""
        <style type="text/css">
          h1 { color : green }
          h2 { color : red }
          b { dir:rtl;color : blue}

        </style>
               
        """+_(u'''   
These are some <b>hints</b> how to use alfanous to get some interested information about ayas of Qur'an

<br>
<ol>
<li> <h2>  Simple search :</h2></li> Write your keywords on the search bar ex: <b>الحمد لله</b>
<br>
<li> <h2>  Search in specified sura :</h2></li> add to your query "sura:" or "سورة:" ex:<b> سورة:الفاتحة </b>
<br>

<li> <h2>  Different methods of sorting:</h2></li> Go to options panel and change "order by" , there are many criteria  : order by relevance, by the position of aya in the Mus-haf ,by the date of revelation ...
<br>
<li> <h2>  Search by a phrase :</h2></li> Write your keywords between double quotes ,ex : <b>"الحمد لله" </b>
<li> <h2>  use logical relations between keywords :</h2></li> 
use + to oblige a keyword ,ex : <b>الصلاة + الزكاة</b>
<br> use - to eliminate a keyword ,ex : <b> الصلاة - الزكاة</b>
<br> use | to search one of  two keywords ,ex :<b> الصلاة | الزكاة</b>

<li> <h2>  use jokers or regular expression :</h2></li>
asterisk  *  replace many letters ,ex :<b> وال* </b>
<br>? replace one letter ,ex:<b> ؟الله</b>


<li> <h2>  search by words of the same origin as a keyword :</h2></li>
use &gt; to search by the infinitive of verbs and the lemma of nouns ,ex:<b> &gt;جاهد </b>
<br>use &gt;&gt; to search by the arabic root  ,ex:<b> &gt;&gt;جاهد </b>
<br>
<li> <h2>  search by vocalization :</h2></li>
for full vocalization,search in the field "aya_" or "آية_" ,ex: <b> آية_:مِنْ</b>
<br>for partial vocalization,search in the field "aya_" or "آية_" using quotes ,ex:<b> آية_:'المَلك' </b>
<br>

<li> <h2>  search by subject :</h2></li>
Go to features panel, Subjects tab 
<br>Ex: search ayas talking about Taloot, choose the chapter :<b> التاريخ و القصص القرآني </b> then the topic :<b> قصة طالوت </b>, choose Relation : "Replace"  and Press "Add to search bar"

<li> <h2>  Structural search :</h2></li>
Go to features panel, Structural search tab 
<br>Ex: for searching only on juz' 3amma, choose search_in : <b>juz's</b> ,from  :<b> 1 </b>, to :<b> 1 </b>. then Relation : "(AND)"  and Press "Add to search bar"

<li> <h2> Statistic search :</h2></li>
Go to features panel, Statistical search tab 
<br>Ex: for searching ayas with more then four names of Allah, choose number_of :<b> Allah words </b>, in : <b>ayas </b>,from  :<b> 5</b> , to :<b> 10 </b>. then Relation : "Replace"  and Press "Add to search bar"

<li> <h2> Search sajadat:</h2></li>
Go to features panel, Divers tab  then choose <b>"yes" </b>for Sajdah

<li> <h2> Verify numeric miracles:</h2></li>
you can use alfanous to verify some numeric miracles of Quran
<br>Ex:  if you search <b>&gt;الدنيا  </b> you find <b>115 </b>times
<br> if you search <b>&gt;الآخرة </b> (includes بالآخرة...)  you find also <b>115 </b>times

</ol>


''')

        try:
            F=open("help.html","r")
        except:
            F=None
        if F:
            html=F.read()
        self.o_results.setText(html)
        
        
TDICT=QUI.traductions_dict(static=False)

def main():
    """ the main function"""
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = QUI()
    ui.setupUi(MainWindow)
    
    MainWindow.show()
    app.exec_()
    ui.exit()

if __name__ == "__main__":
    main()