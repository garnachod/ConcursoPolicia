# -*- coding: utf-8 -*-
import re
import nltk

re_urls = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
re_hastag = re.compile(r'\#[0-9a-zA-Z]+')
re_tuser = re.compile(r'@[a-zA-Z0-9_]+')
re_number = re.compile(r'[0-9]+')


stopwords = {
	"en": {"a":True, "about":True, "above":True, "after":True, "again":True, "against":True, "all":True, "am":True, "an":True, "and":True, "any":True, "are":True, "aren't":True, "as":True, "at":True, "be":True, 
			"because":True, "been":True, "before":True, "being":True, "below":True, "between":True, "both":True, "but":True, "by":True, "can't":True, "cannot":True, "could":True, "couldn't":True, "did":True,
			"didn't":True, "do":True, "does":True, "doesn't":True, "doing":True, "don't":True, "down":True, "during":True, "each":True, "few":True, "for":True, "from":True, "further":True, "had":True, "hadn't":True,
			"has":True, "hasn't":True, "have":True, "haven't":True, "having":True, "he":True, "he'd":True, "he'll":True, "he's":True, "her":True, "here":True, "here's":True, "hers":True, "herself":True, "him":True, 
			"himself":True, "his":True, "how":True, "how's":True, "i":True, "i'd":True, "i'll":True, "i'm":True, "i've":True, "if":True, "in":True, "into":True, "is":True, "isn't":True, "it":True, "it's":True, "its":True, 
			"itself":True, "let's":True, "me":True, "more":True, "most":True, "mustn't":True, "my":True, "myself":True, "no":True, "nor":True, "not":True, "of":True, "off":True, "on":True, "once":True, "only":True, "or":True, 
			"other":True, "ought":True, "our":True, "ours 	ourselves":True, "out":True, "over":True, "own":True, "same":True, "shan't":True, "she":True, "she'd":True, "she'll":True, "she's":True, "should":True, "shouldn't":True, 
			"so":True, "some":True, "such":True, "than":True, "that":True, "that's":True, "the":True, "their":True, "theirs":True, "them":True, "themselves":True, "then":True, "there":True, "there's":True, "these":True, "they":True, 
			"they'd":True, "they'll":True, "they're":True, "they've":True, "this":True, "those":True, "through":True, "to":True, "too":True, "under":True, "until":True, "up":True, "very":True, "was":True, "wasn't":True, "we":True, 
			"we'd":True, "we'll":True, "we're":True, "we've":True, "were":True, "weren't":True, "what":True, "what's":True, "when":True, "when's":True, "where":True, "where's":True, "which":True, "while":True, "who":True, "who's":True, 
			"whom":True, "why":True, "why's":True, "with":True, "won't":True, "would":True, "wouldn't":True, "you":True, "you'd":True, "you'll":True, "you're":True, "you've":True, "your":True, "yours":True, "yourself":True, "yourselves":True},
	
	"es": {"ni":True,"he":True, "os":True, "te":True, "al":True, "mi":True, "tu":True, "le":True, "se":True, "ya":True, "esto":True,"este":True, "tan":True,"son":True, "de":True,"no":True,"me":True, "mas":True, "se":True, "del":True, "un":True, "una":True, "unas":True, "unos":True, "uno":True, "sobre":True, "todo":True, "tambien":True, "tras":True, "otro":True, "algun":True, "alguno":True, "alguna":True, "algunos":True, "algunas":True, "ser":True, "es":True, "soy":True, "eres":True, "somos":True, "sois":True, "estoy":True, "esta":True, "estamos":True, "estais":True, "estan":True, "como":True, "en":True, "para":True, "atras":True, "porque":True, "por":True, "que":True, "estado":True, "estaba":True, "ante":True, "antes":True, "siendo":True, "ambos":True, "pero":True, "por":True, "poder":True, "puede":True, "puedo":True, "podemos":True, "podeis":True, "pueden":True, "fui":True, "fue":True, "fuimos":True, "fueron":True, "hacer":True, "hago":True, "hace":True, "hacemos":True, "haceis":True, "hacen":True, "cada":True, "fin":True, "incluso":True, "primero":True, "desde":True, "conseguir":True, "consigo":True, "consigue":True, "consigues":True, "conseguimos":True, "consiguen":True, "ir":True, "voy":True, "va":True, "vamos":True, "vais":True, "van":True, "vaya":True, "gueno":True, "ha":True, "tener":True, "tengo":True, "tiene":True, "tenemos":True, "teneis":True, "tienen":True, "el":True, "la":True, "lo":True, "las":True, "los":True, "su":True, "aqui":True, "mio":True, "tuyo":True, "ellos":True, "ellas":True, "nos":True, "nosotros":True, "vosotros":True, "vosotras":True, "si":True, "dentro":True, "solo":True, "solamente":True, "saber":True, "sabes":True, "sabe":True, "sabemos":True, "sabeis":True, "saben":True, "ultimo":True, "largo":True, "bastante":True, "haces":True, "muchos":True, "aquellos":True, "aquellas":True, "sus":True, "entonces":True, "tiempo":True, "verdad":True, "verdadero":True, "verdadera":True, "cierto":True, "ciertos":True, "cierta":True, "ciertas":True, "intentar":True, "intento":True, "intenta":True, "intentas":True, "intentamos":True, "intentais":True, "intentan":True, "dos":True, "bajo":True, "arriba":True, "encima":True, "usar":True, "uso":True, "usas":True, "usa":True, "usamos":True, "usais":True, "usan":True, "emplear":True, "empleo":True, "empleas":True, "emplean":True, "ampleamos":True, "empleais":True, "valor":True, "muy":True, "era":True, "eras":True, "eramos":True, "eran":True, "modo":True, "bien":True, "cual":True, "cuando":True, "donde":True, "mientras":True, "quien":True, "con":True, "entre":True, "sin":True, "trabajo":True, "trabajar":True, "trabajas":True, "trabaja":True, "trabajamos":True, "trabajais":True, "trabajan":True, "podria":True, "podrias":True, "podriamos":True, "podrian":True, "podriais":True, "yo":True, "aquel":True},
	"tweet": {"rt":True, "USER":True, "URL": True, "QUESTION":True, "EXCLAMATION":True, "HASTAG":True, "DOTDOTDOT":True, "&amp;": True},
	"fr": {"alors":True, "au":True, "aucuns":True, "aussi":True, "autre":True, "avant":True, "avec":True, "avoir":True, "bon":True, "car":True, "ce":True, "cela":True, "ces":True, "ceux":True, "chaque":True, "ci":True, "comme":True, "comment":True, "dans":True, "des":True, "du":True, "dedans":True, "dehors":True, "depuis":True, "devrait":True, "doit":True, "donc":True, "dos":True, "début":True, "elle":True, "elles":True, "en":True, "encore":True, "essai":True, "est":True, "et":True, "eu":True, "fait":True, "faites":True, "fois":True, "font":True, "hors":True, "ici":True, "il":True, "ils":True, "je":True, "juste":True, "la":True, "le":True, "les":True, "leur":True, "là":True, "ma":True, "maintenant":True, "mais":True, "mes":True, "mine":True, "moins":True, "mon":True, "mot":True, "même":True, "ni":True, "nommés":True, "notre":True, "nous":True, "ou":True, "où":True, "par":True, "parce":True, "pas":True, "peut":True, "peu":True, "plupart":True, "pour":True, "pourquoi":True, "quand":True, "que":True, "quel":True, "quelle":True, "quelles":True, "quels":True, "qui":True, "sa":True, "sans":True, "ses":True, "seulement":True, "si":True, "sien":True, "son":True, "sont":True, "sous":True, "soyez":True, "sujet":True, "sur":True, "ta":True, "tandis":True, "tellement":True, "tels":True, "tes":True, "ton":True, "tous":True, "tout":True, "trop":True, "très":True, "tu":True, "voient":True, "vont":True, "votre":True, "vous":True, "vu":True, "ça":True, "étaient":True, "état":True, "étions":True, "été":True, "être":True},
	"de": {"aber":True, "als":True, "am":True, "an":True, "auch":True, "auf":True, "aus":True, "bei":True, "bin":True, "bis":True, "bist":True, "da":True, "dadurch":True, "daher":True, "darum":True, "das":True, "daß":True, "dass":True, "dein":True, "deine":True, "dem":True, "den":True, "der":True, "des":True, "dessen":True, "deshalb":True, "die":True, "dies":True, "dieser":True, "dieses":True, "doch":True, "dort":True, "du":True, "durch":True, "ein":True, "eine":True, "einem":True, "einen":True, "einer":True, "eines":True, "er":True, "es":True, "euer":True, "eure":True, "für":True, "hatte":True, "hatten":True, "hattest":True, "hattet":True, "hier":True, "hinter":True, "ich":True, "ihr":True, "ihre":True, "im":True, "in":True, "ist":True, "ja":True, "jede":True, "jedem":True, "jeden":True, "jeder":True, "jedes":True, "jener":True, "jenes":True, "jetzt":True, "kann":True, "kannst":True, "können":True, "könnt":True, "machen":True, "mein":True, "meine":True, "mit":True, "muß":True, "mußt":True, "musst":True, "müssen":True, "müßt":True, "nach":True, "nachdem":True, "nein":True, "nicht":True, "nun":True, "oder":True, "seid":True, "sein":True, "seine":True, "sich":True, "sie":True, "sind":True, "soll":True, "sollen":True, "sollst":True, "sollt":True, "sonst":True, "soweit":True, "sowie":True, "und":True, "unser":True, "unsere":True, "unter":True, "vom":True, "von":True, "vor":True, "wann":True, "warum":True, "was":True, "weiter":True, "weitere":True, "wenn":True, "wer":True, "werde":True, "werden":True, "werdet":True, "weshalb":True, "wie":True, "wieder":True, "wieso":True, "wir":True, "wird":True, "wirst":True, "wo":True, "woher":True, "wohin":True, "zu":True, "zum":True, "zur":True, "über":True},
	"ar": {"فى":True, "في":True, "كل":True, "لم":True, "لن":True, "له":True, "من":True, "هو":True, "هي":True, "قوة":True, "كما":True, "لها":True, "منذ":True, "وقد":True, "ولا":True, "نفسه":True, "لقاء":True, "مقابل":True, "هناك":True, "وقال":True, "وكان":True, "نهاية":True, "وقالت":True, "وكانت":True, "للامم":True, "فيه":True, "كلم":True, "لكن":True, "وفي":True, "وقف":True, "ولم":True, "ومن":True, "وهو":True, "وهي":True, "يوم":True, "فيها":True, "منها":True, "مليار":True, "لوكالة":True, "يكون":True, "يمكن":True, "مليون":True, "حيث":True, "اكد":True, "الا":True, "اما":True, "امس":True, "السابق":True, "التى":True, "التي":True, "اكثر":True, "ايار":True, "ايضا":True, "ثلاثة":True, "الذاتي":True, "الاخيرة":True, "الثاني":True, "الثانية":True, "الذى":True, "الذي":True, "الان":True, "امام":True, "ايام":True, "خلال":True, "حوالى":True, "الذين":True, "الاول":True, "الاولى":True, "بين":True, "ذلك":True, "دون":True, "حول":True, "حين":True, "الف":True, "الى":True, "انه":True, "اول":True, "ضمن":True, "انها":True, "جميع":True, "الماضي":True, "الوقت":True, "المقبل":True, "اليوم":True, "ـ":True, "ف":True, "و":True, "و6":True, "قد":True, "لا":True, "ما":True, "مع":True, "مساء":True, "هذا":True, "واحد":True, "واضاف":True, "واضافت":True, "فان":True, "قبل":True, "قال":True},
	"ru": {"а": True, "е": True, "и": True, "ж": True, "м": True, "о": True, "на": True, "не": True, "ни": True, "об": True, "но": True, "он": True, "мне": True, "мои": True, "мож": True, "она": True, "они": True, "оно": True, "мной": True, "много": True, "многочисленное": True, "многочисленная": True, "многочисленные": True, "многочисленный": True, "мною": True, "мой": True, "мог": True, "могут": True, "можно": True, "может": True, "можхо": True, "мор": True, "моя": True, "моё": True, "мочь": True, "над": True, "нее": True, "оба": True, "нам": True, "нем": True, "нами": True, "ними": True, "мимо": True, "немного": True, "одной": True, "одного": True, "менее": True, "однажды": True, "однако": True, "меня": True, "нему": True, "меньше": True, "ней": True, "наверху": True, "него": True, "ниже": True, "мало": True, "надо": True, "один": True, "одиннадцать": True, "одиннадцатый": True, "назад": True, "наиболее": True, "недавно": True, "миллионов": True, "недалеко": True, "между": True, "низко": True, "меля": True, "нельзя": True, "нибудь": True, "непрерывно": True, "наконец": True, "никогда": True, "никуда": True, "нас": True, "наш": True, "нет": True, "нею": True, "неё": True, "них": True, "мира": True, "наша": True, "наше": True, "наши": True, "ничего": True, "начала": True, "нередко": True, "несколько": True, "обычно": True, "опять": True, "около": True, "мы": True, "ну": True, "нх": True, "от": True, "отовсюду": True, "особенно": True, "нужно": True, "очень": True, "отсюда": True, "в": True, "во": True, "вон": True, "вниз": True, "внизу": True, "вокруг": True, "вот": True, "восемнадцать": True, "восемнадцатый": True, "восемь": True, "восьмой": True, "вверх": True, "вам": True, "вами": True, "важное": True, "важная": True, "важные": True, "важный": True, "вдали": True, "везде": True, "ведь": True, "вас": True, "ваш": True, "ваша": True, "ваше": True, "ваши": True, "впрочем": True, "весь": True, "вдруг": True, "вы": True, "все": True, "второй": True, "всем": True, "всеми": True, "времени": True, "время": True, "всему": True, "всего": True, "всегда": True, "всех": True, "всею": True, "всю": True, "вся": True, "всё": True, "всюду": True, "г 	год": True, "говорил": True, "говорит": True, "года": True, "году": True, "где": True, "да": True, "ее": True, "за": True, "из": True, "ли": True, "же": True, "им": True, "до": True, "по": True, "ими": True, "под": True, "иногда": True, "довольно": True, "именно": True, "долго": True, "позже": True, "более": True, "должно": True, "пожалуйста": True, "значит": True, "иметь": True, "больше": True, "пока": True, "ему": True, "имя": True, "пор": True, "пора": True, "потом": True, "потому": True, "после": True, "почему": True, "почти": True, "посреди": True, "ей": True, "два": True, "две": True, "двенадцать": True, "двенадцатый": True, "двадцать": True, "двадцатый": True, "двух": True, "его": True, "дел": True, "или": True, "без": True, "день": True, "занят": True, "занята": True, "занято": True, "заняты": True, "действительно": True, "давно": True, "девятнадцать": True, "девятнадцатый": True, "девять": True, "девятый": True, "даже": True, "алло": True, "жизнь": True, "далеко": True, "близко": True, "здесь": True, "дальше": True, "для": True, "лет": True, "зато": True, "даром": True, "первый": True, "перед": True, "затем": True, "зачем": True, "лишь": True, "десять": True, "десятый": True, "ею": True, "её": True, "их": True, "бы": True, "еще": True, "при": True, "был": True, "про": True, "процентов": True, "против": True, "просто": True, "бывает": True, "бывь": True, "если": True, "люди": True, "была": True, "были": True, "было": True, "будем": True, "будет": True, "будете": True, "будешь": True, "прекрасно": True, "буду": True, "будь": True, "будто": True, "будут": True, "ещё": True, "пятнадцать": True, "пятнадцатый": True, "друго": True, "другое": True, "другой": True, "другие": True, "другая": True, "других": True, "есть": True, "пять": True, "быть": True, "лучше": True, "пятый": True, "к": True, "ком": True, "конечно": True, "кому": True, "кого": True, "когда": True, "которой": True, "которого": True, "которая": True, "которые": True, "который": True, "которых": True, "кем": True, "каждое": True, "каждая": True, "каждые": True, "каждый": True, "кажется": True, "как": True, "какой": True, "какая": True, "кто": True, "кроме": True, "куда": True, "кругом": True, "с 	т": True, "у": True, "я": True, "та": True, "те": True, "уж": True, "со": True, "то": True, "том": True, "снова": True, "тому": True, "совсем": True, "того": True, "тогда": True, "тоже": True, "собой": True, "тобой": True, "собою": True, "тобою": True, "сначала": True, "только": True, "уметь": True, "тот": True, "тою": True, "хорошо": True, "хотеть": True, "хочешь": True, "хоть": True, "хотя": True, "свое": True, "свои": True, "твой": True, "своей": True, "своего": True, "своих": True, "свою": True, "твоя": True, "твоё": True, "раз": True, "уже": True, "сам": True, "там": True, "тем": True, "чем": True, "сама": True, "сами": True, "теми": True, "само": True, "рано": True, "самом": True, "самому": True, "самой": True, "самого": True, "семнадцать": True, "семнадцатый": True, "самим": True, "самими": True, "самих": True, "саму": True, "семь": True, "чему": True, "раньше": True, "сейчас": True, "чего": True, "сегодня": True, "себе": True, "тебе": True, "сеаой": True, "человек": True, "разве": True, "теперь": True, "себя": True, "тебя": True, "седьмой": True, "спасибо": True, "слишком": True, "так": True, "такое": True, "такой": True, "такие": True, "также": True, "такая": True, "сих": True, "тех": True, "чаще": True, "четвертый": True, "через": True, "часто": True, "шестой": True, "шестнадцать": True, "шестнадцатый": True, "шесть": True, "четыре": True, "четырнадцать": True, "четырнадцатый": True, "сколько": True, "сказал": True, "сказала": True, "сказать": True, "ту": True, "ты": True, "три": True, "эта": True, "эти": True, "что": True, "это": True, "чтоб": True, "этом": True, "этому": True, "этой": True, "этого": True, "чтобы": True, "этот": True, "стал": True, "туда": True, "этим": True, "этими": True, "рядом": True, "тринадцать": True, "тринадцатый": True, "этих": True, "третий": True, "тут": True, "эту": True, "суть": True, "чуть": True, "тысяч" : True}
}


"""languages = ("danish", "dutch", "english", "finnish", "french", "german",
                 "hungarian", "italian", "norwegian", "porter", "portuguese",
                 "romanian", "russian", "spanish", "swedish")"""

stemmers = {
	"en": nltk.stem.snowball.SnowballStemmer("english"),
	"es": nltk.stem.snowball.SnowballStemmer("spanish"),
	"de": nltk.stem.snowball.SnowballStemmer("german"),
	"fr": nltk.stem.snowball.SnowballStemmer("french"),
	"ru": nltk.stem.snowball.SnowballStemmer("russian"),
	"ar": nltk.stem.isri.ISRIStemmer()
}

class LimpiadorTweets(object):
	@staticmethod
	def clean(line):
		line = line.lower()
		line = line.replace("\n", ". ").replace("\r", ". ").replace(u"\u0085", ". ").replace(u"\u2028", ". ").replace(u"\u2029", ". ")
		line = re_urls.sub(" URL ", line)
		line = re_hastag.sub(" HASTAG ", line)
		line = re_tuser.sub(" USER ", line)
		line = re_number.sub(" ", line)
		line = line.replace("?", " QUESTION ")
		line = line.replace(u"¿", " QUESTION ")
		line = line.replace("!", " EXCLAMATION ")
		line = line.replace(u"¡", " EXCLAMATION ")
		line = line.replace("...", " DOTDOTDOT ")
		#line = line.replace(".", " DOT ")
		#line = line.replace(",", " COMMA ")
		line = line.replace(".", " ")
		line = line.replace(",", " ")
		line = line.replace("/", " ")
		line = line.replace("\\", " ")
		line = line.replace("\"", " ")
		line = line.replace("-", " ")
		line = line.replace(u"&", " ")
		line = line.replace(";", " ")
		line = line.replace(")", " ")
		line = line.replace("(", " ")
		line = line.replace("'", " ")
		line = line.replace(":", " ")
		line = line.replace(u"’", " ")
		line = line.replace(u"‘", " ")
		line = line.replace(u"º", " ")
		line = line.replace("+", " ")
		line = line.replace("_", " ")
		line = line.replace(u"´", " ")
		line = line.replace(u"`", " ")
		line = line.replace(u"", " ")
		line = line.replace(u"", " ")
		line = line.replace(u"", " ")
		line = line.replace(u"", " ")
		line = line.replace(u"🐾", " ")
		line = line.replace(u"🙈", " ")
		line = line.replace(u"⛄", " ")
		line = line.replace(u"💋", " ")
		line = line.replace(u"🎄", " ")
		line = line.replace(u"✌", " ")
		line = line.replace(u"—", " ")
		line = line.replace(u"✈", " ")
		line = line.replace(u"✅", " ")
		line = line.replace(u"😂", " ")
		line = line.replace(u"😜", " ")
		line = line.replace(u"😍", " ")
		line = line.replace(u"️", " ")
		line = line.replace(u"❤", " ")
		line = line.replace(u"«", " ")
		line = line.replace(u"»", " ")
		line = line.replace(u"“", " ")
		line = line.replace(u"”", " ")
		line = line.replace(u"¨", " ")
		line = line.replace(u"á", "a")
		line = line.replace(u"é", "e")
		line = line.replace(u"í", "i")
		line = line.replace(u"ó", "o")
		line = line.replace(u"ú", "u")
		line = line.replace(u"ü", "u")
		line = line.replace(u"ñ", "n")
		line = line.replace(u"…", " ")
		line = line.replace("https", " ")
		line = line.replace("http", " ")
		line = line.replace("  ", " ")
		line = line.replace("  ", " ")
		line = line.replace("  ", " ")
		line = line.replace("  ", " ")


		return line

	@staticmethod
	def stopWordsByLanguagefilter(line, lang):
		if lang in stopwords:
			fraseFinal = u""
			for palabra in line.split():
				if palabra in stopwords[lang] or palabra in stopwords["tweet"]:
					pass
				else:
					if len(palabra) > 1:
						fraseFinal += palabra + " "

			return fraseFinal
		else:
			fraseFinal = u""
			for palabra in line.split():
				if palabra in stopwords["tweet"]:
					pass
				else:
					if len(palabra) > 1:
						fraseFinal += palabra + " "

			return fraseFinal

	@staticmethod
	def stemmingByLanguage(line, lang):
		if lang in stemmers:
			fraseFinal = u""
			for palabra in line.split():
				fraseFinal += stemmers[lang].stem(palabra) + " "

			return fraseFinal

		return line