from flask import Flask, request, jsonify, render_template
from pyspark.sql import SparkSession
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

text = """
{{Short description|Political philosophy and movement}}
{{Other uses|Anarchy|Anarchism (disambiguation)|Anarchist (disambiguation)}}
{{Pp-semi-indef}}
{{Good article}}
{{Use British English|date=August 2021}}
{{Use dmy dates|date=August 2021}}
{{Use shortened footnotes|date=May 2023}}
{{Anarchism sidebar}}

'''Anarchism''' is a [[political philosophy]] and [[Political movement|movement]] that is against all forms of [[authority]] and seeks to abolish the [[institutions]] it claims maintain unnecessary [[coercion]] and [[Social hierarchy|hierarchy]], typically including the [[state (polity)|state]] and [[capitalism]]. Anarchism advocates for the replacement of the state with [[Stateless society|stateless societies]] and [[Voluntary association|voluntary]] [[Free association (communism and anarchism)|free associations]]. As a historically [[left-wing]] movement, this reading of anarchism is placed on the [[Far-left politics|farthest left]] of the [[political spectrum]], usually described as the [[libertarian]] wing of the [[socialist movement]] ([[libertarian socialism]]).

Although traces of anarchist ideas are found all throughout history, modern anarchism emerged from the [[Age of Enlightenment|Enlightenment]]. During the latter half of the 19th and the first decades of the 20th century, the anarchist movement flourished in most parts of the world and had a significant role in workers' struggles for [[emancipation]]. [[#Schools of thought|Various anarchist schools of thought]] formed during this period. Anarchists have taken part in several revolutions, most notably in the [[Paris Commune]], the [[Russian Civil War]] and the [[Spanish Civil War]], whose end marked the end of the [[classical era of anarchism]]. In the last decades of the 20th and into the 21st century, the anarchist movement has been resurgent once more, growing in popularity and influence within [[anti-capitalist]], [[anti-war]] and [[anti-globalisation]] movements.

Anarchists employ [[diversity of tactics|diverse approaches]], which may be generally divided into revolutionary and [[evolutionary strategies]]; there is significant overlap between the two. Evolutionary methods try to simulate what an anarchist society might be like, but revolutionary tactics, which have historically taken a violent turn, aim to overthrow authority and the state. Many facets of human civilization have been influenced by anarchist theory, critique, and [[Praxis (process)|praxis]].
{{Toc limit|3}}

== Etymology, terminology, and definition ==
{{Main|Definition of anarchism and libertarianism}}
{{See also|Glossary of anarchism}}
[[File:WilhelmWeitling.jpg|thumb|[[Wilhelm Weitling]] is an example of a writer who added to anarchist theory without using the exact term.{{Sfn|Carlson|1972|pp=22–23}}]]
The etymological origin of ''anarchism'' is from the Ancient Greek ''anarkhia'' (ἀναρχία), meaning &quot;without a ruler&quot;, composed of the prefix ''an-'' (&quot;without&quot;) and the word ''arkhos'' (&quot;leader&quot; or &quot;ruler&quot;). The suffix ''[[-ism]]'' denotes the ideological current that favours [[anarchy]].{{Sfnm|1a1=Bates|1y=2017|1p=128|2a1=Long|2y=2013|2p=217}} ''Anarchism'' appears in English from 1642 as ''anarchisme'' and ''anarchy'' from 1539; early English usages emphasised a sense of disorder.{{Sfnm|1a1=Merriam-Webster|1y=2019|1loc=&quot;Anarchism&quot;|2a1=''Oxford English Dictionary''|2y=2005|2loc=&quot;Anarchism&quot;|3a1=Sylvan|3y=2007|3p=260}} Various factions within the [[French Revolution]] labelled their opponents as ''anarchists'', although few such accused shared many views with later anarchists. Many revolutionaries of the 19th century such as [[William Godwin]] (1756–1836) and [[Wilhelm Weitling]] (1808–1871) would contribute to the anarchist doctrines of the next generation but did not use ''anarchist'' or ''anarchism'' in describing themselves or their beliefs.{{Sfn|Joll|1964|pp=27–37}}

The first political philosopher to call himself an ''anarchist'' ({{Lang-fr|anarchiste}}) was [[Pierre-Joseph Proudhon]] (1809–1865), marking the formal birth of anarchism in the mid-19th century. Since the 1890s and beginning in France,{{Sfn|Nettlau|1996|p=162}} ''[[libertarianism]]'' has often been used as a synonym for anarchism{{Sfn|Guérin|1970|loc=&quot;The Basic Ideas of Anarchism&quot;}} and its use as a synonym is still common outside the United States.{{Sfnm|1a1=Ward|1y=2004|1p=62|2a1=Goodway|2y=2006|2p=4|3a1=Skirda|3y=2002|3p=183|4a1=Fernández|4y=2009|4p=9}} Some usages of ''libertarianism'' refer to [[individualistic]] [[free-market]] philosophy only, and [[free-market anarchism]] in particular is termed ''libertarian anarchism''.{{Sfn|Morris|2002|p=61}}

While the term ''libertarian'' has been largely synonymous with anarchism,{{Sfnm|1a1=Marshall|1y=1992|1p=641|2a1=Cohn|2y=2009|2p=6}} its meaning has more recently been diluted by wider adoption from ideologically disparate groups,{{Sfn|Marshall|1992|p=641}} including both the [[New Left]] and [[libertarian Marxists]], who do not associate themselves with [[authoritarian socialists]] or a [[vanguard party]], and extreme [[cultural liberals]], who are primarily concerned with [[civil liberties]].{{Sfn|Marshall|1992|p=641}} Additionally, some anarchists use ''[[libertarian socialist]]''{{Sfnm|1a1=Marshall|1y=1992|1p=641|2a1=Cohn|2y=2009|2p=6|3a1=Levy|3a2=Adams|3y=2018|3p=104}} to avoid anarchism's negative connotations and emphasise its connections with [[socialism]].{{Sfn|Marshall|1992|p=641}} ''Anarchism'' is broadly used to describe the [[anti-authoritarian]] wing of the [[socialist movement]].{{Sfn|Levy|Adams|2018|p=104}}{{Refn|In ''Anarchism: From Theory to Practice'' (1970),{{Sfn|Guérin|1970|p=12}} anarchist historian [[Daniel Guérin]] described it as a synonym for [[libertarian socialism]], and wrote that anarchism &quot;is really a synonym for socialism. The anarchist is primarily a socialist whose aim is to abolish the exploitation of man by man. Anarchism is only one of the streams of socialist thought, that stream whose main components are concern for liberty and haste to abolish the State.&quot;{{Sfn|Arvidsson|2017}} In his many works on anarchism, historian [[Noam Chomsky]] describes anarchism, alongside [[libertarian Marxism]], as the [[libertarian]] wing of [[socialism]].{{Sfn|Otero|1994|p=617}}|group=nb}} Anarchism is contrasted to socialist forms which are state-oriented or from above.{{Sfn|Osgood|1889|p=1}} Scholars of anarchism generally highlight anarchism's socialist credentials{{Sfn|Newman|2005|p=15}} and criticise attempts at creating dichotomies between the two.{{Sfn|Morris|2015|p=64}} Some scholars describe anarchism as having many influences from [[liberalism]],{{Sfn|Marshall|1992|p=641}} and being both liberal and socialist but more so.{{Sfn|Walter|2002|p=44}} Many scholars reject [[anarcho-capitalism]] as a misunderstanding of anarchist principles.{{Sfnm|1a1=Marshall|1y=1992|1pp=564–565|2a1=Jennings|2y=1993|2p=143|3a1=Gay|3a2=Gay|3y=1999|3p=15|4a1=Morris|4y=2008|4p=13|5a1=Johnson|5y=2008|5p=169|6a1=Franks|6y=2013|6pp=393–394}}{{Refn|[[Herbert L. Osgood]] claimed that anarchism is &quot;the extreme antithesis&quot; of [[authoritarian communism]] and [[state socialism]].{{Sfn|Osgood|1889|p=1}} [[Peter Marshall (author)|Peter Marshall]] states that &quot;[i]n general anarchism is closer to socialism than liberalism. ... Anarchism finds itself largely in the socialist camp, but it also has outriders in liberalism. It cannot be reduced to socialism, and is best seen as a separate and distinctive doctrine.&quot;{{Sfn|Marshall|1992|p=641}} According to [[Jeremy Jennings]], &quot;[i]t is hard not to conclude that these ideas&quot;, referring to [[anarcho-capitalism]], &quot;are described as anarchist only on the basis of a misunderstanding of what anarchism is.&quot; Jennings adds that &quot;anarchism does not stand for the untrammelled freedom of the individual (as the 'anarcho-capitalists' appear to believe) but, as we have already seen, for the extension of individuality and community.&quot;{{Sfn|Jennings|1999|p=147}} [[Nicolas Walter]] wrote that &quot;anarchism does derive from liberalism and socialism both historically and ideologically. ... In a sense, anarchists always remain liberals and socialists, and whenever they reject what is good in either they betray anarchism itself. ... We are liberals but more so, and socialists but more so.&quot;{{Sfn|Walter|2002|p=44}} Michael Newman includes anarchism as one of many [[socialist traditions]], especially the more socialist-aligned tradition following Proudhon and [[Mikhail Bakunin]].{{Sfn|Newman|2005|p=15}} [[Brian Morris (anthropologist)|Brian Morris]] argues that it is &quot;conceptually and historically misleading&quot; to &quot;create a dichotomy between socialism and anarchism.&quot;{{Sfn|Morris|2015|p=64}}|group=nb}}

While [[Anti-statism|opposition to the state]] is central to anarchist thought, defining ''anarchism'' is not an easy task for scholars, as there is a lot of discussion among scholars and anarchists on the matter, and various currents perceive anarchism slightly differently.{{Sfn|Long|2013|p=217}}{{Refn|One common definition adopted by anarchists is that anarchism is a cluster of political philosophies opposing [[authority]] and [[hierarchical organisation]], including [[Anarchism and capitalism|capitalism]], [[Anarchism and nationalism|nationalism]], the [[State (polity)|state]], and all associated [[institution]]s, in the conduct of all [[human relations]] in favour of a society based on [[decentralisation]], [[freedom]], and [[voluntary association]]. Scholars highlight that this definition has the same shortcomings as the definition based on anti-authoritarianism (''[[a posteriori]]'' conclusion), anti-statism (anarchism is much more than that),{{Sfnm|1a1=McLaughlin|1y=2007|1p=166|2a1=Jun|2y=2009|2p=507|3a1=Franks|3y=2013|3pp=386–388}} and etymology (negation of rulers).{{Sfnm|1a1=McLaughlin|1y=2007|1pp=25–29|2a1=Long|2y=2013|2pp=217}}|group=nb}} Major definitional elements include the will for a non-coercive society, the rejection of the state apparatus, the belief that human nature allows humans to exist in or progress toward such a non-coercive society, and a suggestion on how to act to pursue the ideal of anarchy.{{Sfn|McLaughlin|2007|pp=25–26}}

== History ==
{{Main|History of anarchism}}

=== Pre-modern era ===
[[File:Paolo Monti - Servizio fotografico (Napoli, 1969) - BEIC 6353768.jpg|thumb|upright=.7|[[Zeno of Citium]] ({{Circa|334|262 BC}}), whose ''[[Republic (Zeno)|Republic]]'' inspired [[Peter Kropotkin]]{{Sfn|Marshall|1993|p=70}}]]
The most notable precursors to anarchism in the ancient world were in China and Greece. In China, [[philosophical anarchism]] (the discussion on the legitimacy of the state) was delineated by [[Taoism|Taoist]] philosophers [[Zhuang Zhou]] and [[Laozi]].{{Sfnm|1a1=Coutinho|1y=2016|2a1=Marshall|2y=1993|2p=54}} Alongside [[Stoicism]], Taoism has been said to have had &quot;significant anticipations&quot; of anarchism.{{Sfn|Sylvan|2007|p=257}}

Anarchic attitudes were also articulated by tragedians and philosophers in Greece. [[Aeschylus]] and [[Sophocles]] used the myth of [[Antigone]] to illustrate the conflict between laws imposed by the state and personal [[autonomy]]. [[Socrates]] questioned [[Athens|Athenian]] authorities constantly and insisted on the right of individual freedom of conscience. [[Cynicism (philosophy)|Cynics]] dismissed human law (''[[Nomos (sociology)|nomos]]'') and associated authorities while trying to live according to nature (''[[physis]]''). [[Stoics]] were supportive of a society based on unofficial and friendly relations among its citizens without the presence of a state.{{Sfn|Marshall|1993|pp=4, 66–73}}

In [[Middle Ages|medieval Europe]], there was no anarchistic activity except some ascetic religious movements. These, and other Muslim movements, later gave birth to [[Anarchism and religion|religious anarchism]]. In the [[Sasanian Empire]], [[Mazdak]] called for an [[egalitarian]] society and the [[abolition of monarchy]], only to be soon executed by Emperor [[Kavad I]].{{Sfn|Marshall|1993|p=86}}

In [[Basra]], religious sects preached against the state.{{Sfn|Crone|2000|pp=3, 21–25}} In Europe, various sects developed anti-state and libertarian tendencies.{{Sfn|Nettlau|1996|p=8}} Renewed interest in antiquity during the [[Renaissance]] and in private judgment during the [[Reformation]] restored elements of anti-authoritarian secularism, particularly in France.{{Sfn|Marshall|1993|p=108}} [[Age of Enlightenment|Enlightenment]] challenges to intellectual authority (secular and religious) and the [[List of revolutions and rebellions|revolutions of the 1790s and 1848]] all spurred the ideological development of what became the era of classical anarchism.{{Sfn|Levy|Adams|2018|p=307}}

=== Modern era ===
During the [[French Revolution]], partisan groups such as the [[Enragés]] and the {{Lang|fr|[[sans-culottes]]}} saw a turning point in the fermentation of anti-state and federalist sentiments.{{Sfn|Marshall|1993|p=4}} The first anarchist currents developed throughout the 18th century as [[William Godwin]] espoused [[philosophical anarchism]] in England, morally delegitimising the state, [[Max Stirner]]'s thinking paved the way to [[Individualist anarchism|individualism]] and [[Pierre-Joseph Proudhon]]'s theory of [[Mutualism (economic theory)|mutualism]] found fertile soil in France.{{Sfn|Marshall|1993|pp=4–5}} By the late 1870s, various anarchist schools of thought had become well-defined and a wave of then unprecedented [[globalisation]] occurred from 1880 to 1914.{{Sfn|Levy|2011|pp=10–15}} This era of [[classical anarchism]] lasted until the end of the [[Spanish Civil War]] and is considered the golden age of anarchism.{{Sfn|Marshall|1993|pp=4–5}}

[[File:Bakunin.png|thumb|upright|Mikhail Bakunin opposed the Marxist aim of [[dictat  orship of the proletariat]] and allied himself with the federalists in the First International before his expulsion by the Marxists.]]
Drawing from mutualism, [[Mikhail Bakunin]] founded [[collectivist anarchism]] and entered the [[International Workingmen's Association]], a class worker union later known as the First International that formed in 1864 to unite diverse revolutionary currents. The International became a significant political force, with [[Karl Marx]] being a leading figure and a member of its General Council. Bakunin's faction (the [[Jura Federation]]) and Proudhon's followers (the mutualists) opposed [[state socialism]], advocating political [[abstentionism]] and small property holdings.{{Sfnm|1a1=Dodson|1y=2002|1p=312|2a1=Thomas|2y=1985|2p=187|3a1=Chaliand|3a2=Blin|3y=2007|3p=116}} After bitter disputes, the Bakuninists were expelled from the International by the [[Marxists]] at the [[1872 Hague Congress]].{{Sfnm|1a1=Graham|1y=2019|1pp=334–336|2a1=Marshall|2y=1993|2p=24}} Anarchists were treated similarly in the [[Second International]], being ultimately expelled in 1896.{{Sfn|Levy|2011|p=12}} Bakunin predicted that if revolutionaries gained power by Marx's terms, they would end up the new tyrants of workers. In response to their expulsion from the First International, anarchists formed the [[St. Imier International]]. Under the influence of [[Peter Kropotkin]], a Russian philosopher and scientist, [[anarcho-communism]] overlapped with collectivism.{{Sfn|Marshall|1993|p=5}} Anarcho-communists, who drew inspiration from the 1871 [[Paris Commune]], advocated for free federation and for the distribution of goods according to one's needs.{{Sfn|Graham|2005|p=xii}}

By the turn of the 20th century, anarchism had spread all over the world.{{Sfn|Moya|2015|p=327}} It was a notable feature of the international syndicalist movement.{{Sfn|Levy|2011|p=16}} In China, small groups of students imported the humanistic pro-science version of anarcho-communism.{{Sfn|Marshall|1993|pp=519–521}} Tokyo was a hotspot for [[rebellion|rebellious]] youth from [[East Asia]]n countries, who moved to the Japanese capital to study.{{Sfnm|1a1=Dirlik|1y=1991|1p=133|2a1=Ramnath|2y=2019|2pp=681–682}} In [[Latin America]], [[Anarchism in Argentina|Argentina]] was a stronghold for [[anarcho-syndicalism]], where it became the most prominent left-wing ideology.{{Sfnm|1a1=Levy|1y=2011|1p=23|2a1=Laursen|2y=2019|2p=157|3a1=Marshall|3y=1993|3pp=504–508}} During this time, a minority of anarchists adopted tactics of revolutionary [[political violence]], known as [[propaganda of the deed]].{{Sfn|Marshall|1993|pp=633–636}} The dismemberment of the French socialist movement into many groups and the execution and exile of many [[Communards]] to penal colonies following the suppression of the Paris Commune favoured individualist political expression and acts.{{Sfn|Anderson|2004}} Even though many anarchists distanced themselves from these terrorist acts, infamy came upon the movement and attempts were made to prevent anarchists immigrating to the US, including the [[Immigration Act of 1903]], also called the Anarchist Exclusion Act.{{Sfnm|1a1=Marshall|1y=1993|1pp=633–636|2a1=Lutz|2a2=Ulmschneider|2y=2019|2p=46}} [[Illegalism]] was another strategy which some anarchists adopted during this period.{{Sfn|Bantman|2019|p=374}}

[[File:Makhno group.jpg|thumb|right|Nestor Makhno seen with members of the anarchist [[Revolutionary Insurgent Army of Ukraine]]]]
Despite concerns, anarchists enthusiastically participated in the [[Russian Revolution]] in opposition to the [[White movement]], especially in the [[Makhnovshchina]]; however, they met harsh suppression after the [[Bolshevik government]] had stabilised, including during the [[Kronstadt rebellion]].{{Sfn|Avrich|2006|p=204}} Bolshevik repressions of anarchist organizations [[Explosion in Leontievsky Lane|prompted a series of assassination attempts on the Russian Communist leadership]].{{Sfn|Grossman|2020|p=230}} Several anarchists from Petrograd and Moscow fled to Ukraine, before the Bolsheviks crushed the anarchist movement there too.{{Sfn|Avrich|2006|p=204}} With the anarchists being repressed in Russia, two new antithetical currents emerged, namely [[platformism]] and [[synthesis anarchism]]. The former sought to create a coherent group that would push for revolution while the latter were against anything that would resemble a political party. Seeing the victories of the [[Bolsheviks]] in the [[October Revolution]] and the resulting [[Russian Civil War]], many workers and activists turned to [[communist parties]] which grew at the expense of anarchism and other socialist movements. In France and the United States, members of major syndicalist movements such as the [[General Confederation of Labour (France)|General Confederation of Labour]] and the [[Industrial Workers of the World]] left their organisations and joined the [[Communist International]].{{Sfn|Nomad|1966|p=88}}

In the [[Spanish Civil War]] of 1936–39, anarchists and syndicalists ([[Confederación Nacional del Trabajo|CNT]] and [[Federación Anarquista Ibérica|FAI]]) once again allied themselves with various currents of leftists. A long tradition of [[Spanish anarchism]] led to anarchists playing a pivotal role in the war, and particularly in the [[Spanish Revolution of 1936]]. In response to the army [[rebellion]], an anarchist-inspired movement of peasants and workers, supported by armed militias, took control of Barcelona and of large areas of rural Spain, where they [[collectivised]] the land.{{Sfn|Bolloten|1984|p=1107}} The [[Soviet Union]] provided some limited assistance at the beginning of the war, but the result was a bitter fight between communists and other leftists in a series of events known as the [[May Days]], as Joseph Stalin asserted Soviet control of the [[Republican faction (Spanish Civil War)|Republican]] government, ending in another defeat of anarchists at the hands of the communists.{{Sfn|Marshall|1993|pp=xi, 466}}

==== Post-WWII ====
[[File:Rojava Sewing Cooperative.jpg|thumb|Rojava's support efforts for workers to form cooperatives is exemplified in this sewing cooperative.]]
By the end of [[World War II]], the anarchist movement had been severely weakened.{{Sfn|Marshall|1993|p=xi}} The 1960s witnessed a revival of anarchism, likely caused by a perceived failure of [[Marxism–Leninism]] and tensions built by the [[Cold War]].{{Sfn|Marshall|1993|p=539}} During this time, anarchism found a presence in other movements critical towards both capitalism and the state such as the [[Anti-nuclear movement|anti-nuclear]], [[Environmental movement|environmental]], and [[peace movement]]s, the [[counterculture of the 1960s]], and the [[New Left]].{{Sfn|Marshall|1993|pp=xi, 539}} It also saw a transition from its previous revolutionary nature to provocative [[anti-capitalist reform]]ism.{{Sfn|Levy|2011|pp=5|p=}} Anarchism became associated with [[punk subculture]] as exemplified by bands such as [[Crass]] and the [[Sex Pistols]].{{Sfn|Marshall|1993|pp=493–494}} The established [[feminist]] tendencies of [[anarcha-feminism]] returned with vigour during the [[second wave of feminism]].{{Sfn|Marshall|1993|pp=556–557}} [[Black anarchism]] began to take form at this time and influenced anarchism's move from a [[Eurocentric]] demographic.{{Sfn|Williams|2015|p=680}} This coincided with its failure to gain traction in Northern Europe and its unprecedented height in Latin America.{{Sfn|Harmon|2011|p=70}}

Around the turn of the 21st century, anarchism grew in popularity and influence within anti-capitalist, anti-war and [[anti-globalisation]] movements.{{Sfn|Rupert|2006|p=66}} Anarchists became known for their involvement in protests against the [[World Trade Organization]] (WTO), the [[Group of Eight]] and the [[World Economic Forum]]. During the protests, ''ad hoc'' leaderless anonymous cadres known as [[black bloc]]s engaged in [[riot]]ing, [[property destruction]] and violent confrontations with the [[police]]. Other organisational tactics pioneered at this time include [[affinity group]]s, [[security culture]] and the use of decentralised technologies such as the Internet. A significant event of this period was the confrontations at the [[1999 Seattle WTO conference]].{{Sfn|Rupert|2006|p=66}} Anarchist ideas have been influential in the development of the [[Zapatista Army of National Liberation|Zapatistas]] in Mexico and the Democratic Federation of Northern Syria, more commonly known as [[Rojava]], a ''de facto'' [[Permanent autonomous zone|autonomous region]] in northern Syria.{{Sfn|Ramnath|2019|p=691}}

While having revolutionary aspirations, many forms of anarchism are not confrontational nowadays. Instead, they are trying to build an alternative way of social organization, based on mutual interdependence and voluntary cooperation. Scholar Carissa Honeywell takes the example of [[Food not Bombs]] group of collectives, to highlight some features of how anarchist groups work: direct action, working together and in solidarity with those left behind. While doing so, they inform about the rising rates of world hunger suggest a policy to tackle hunger, ranging from de-funding the arms industry to addressing Monsanto seed-saving policies and patents, helping farmers and commodification of food and housing.{{Sfn|Honeywell|2021|pp=34–44}} Honeywell also emphasizes that contemporary anarchists are interested in the flourishing not only of humans, but non-humans and the environment as well.{{Sfn|Honeywell|2021|pp=1–2}} Honeywell argues that escalation of problems such as continuous wars and world poverty show that the current framework not only cannot solve those pressing problems for humanity, but are causal factors as well, resulting in the rejection of representative democracy and the state as a whole.{{Sfn|Honeywell|2021|pp=1–3}}
"""

# Tạo endpoint để phục vụ trang web chính
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Endpoint xử lý API
@app.route('/query', methods=['POST'])
def process_query():
    user_query = request.json.get("query", "")
    print(user_query)
    try:
        return jsonify({"title": "success", "text": text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)