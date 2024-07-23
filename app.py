from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
import asyncio
app = Flask(__name__)
engine = pyttsx3.init()


general_crime_cases = {
     "attempt to murder": "The punishment for attempt to murder, as per Section 307 of the Indian Penal Code (IPC), involves imprisonment which may extend to ten years, and also be liable to fine.",
    "voluntarily causing hurt": "The punishment for voluntarily causing hurt, as per Section 323 of the Indian Penal Code (IPC), involves simple imprisonment which may extend to one year, or with fine which may extend to one thousand rupees, or with both.",
    "voluntarily causing grievous hurt": "The punishment for voluntarily causing grievous hurt, as per Section 325 of the Indian Penal Code (IPC), involves imprisonment which may extend to seven years, or with fine which may extend to two thousand rupees, or with both.",
    "kidnapping or abducting women to compel her marriage": "The punishment for kidnapping or abducting women to compel her marriage, as per Section 366 of the Indian Penal Code (IPC), involves imprisonment which may extend to ten years, and shall also be liable to fine.",
    "wrongful restraint": "The punishment for wrongful restraint, as per Section 339 of the Indian Penal Code (IPC), involves simple imprisonment which may extend to one month, or with fine which may extend to five hundred rupees, or with both.",
    "wrongful confinement": "The punishment for wrongful confinement, as per Section 342 of the Indian Penal Code (IPC), involves simple imprisonment which may extend to one year, or with fine which may extend to one thousand rupees, or with both.",
    "criminal breach of trust": "The punishment for criminal breach of trust, as per Section 406 of the Indian Penal Code (IPC), involves imprisonment of either description for a term which may extend to three years, or with fine, or with both.",
    "cheating": "The punishment for cheating, as per Section 415 of the Indian Penal Code (IPC), involves imprisonment of either description for a term which may extend to one year, or with fine, or with both.",
    "forgery": "The punishment for forgery, as per Section 463 of the Indian Penal Code (IPC), involves imprisonment of either description for a term which may extend to two years, or with fine, or with both.",
    "counterfeiting": "The punishment for counterfeiting, as per Section 489 of the Indian Penal Code (IPC), involves imprisonment of either description for a term which may extend to seven years, or with fine, or with both.",
    "criminal intimidation": "The punishment for criminal intimidation, as per Section 506 of the Indian Penal Code (IPC), involves imprisonment which may extend to two years, or with fine, or with both.",
    "sexual harassment": "The punishment for sexual harassment, as per Section 354A of the Indian Penal Code (IPC), involves imprisonment which may extend to three years, or with fine, or with both.",
    "domestic violence": "The punishment for domestic violence, as per the Protection of Women from Domestic Violence Act, 2005, may include imprisonment which may extend to three years, and also be liable to fine.",
    "human trafficking": "The punishment for human trafficking, as per the Immoral Traffic (Prevention) Act, 1956, varies depending on the specific offense but may include imprisonment and fines.",
    "attempt to commit suicide": "The punishment for attempt to commit suicide, as per Section 309 of the Indian Penal Code (IPC), involves simple imprisonment for a term which may extend to one year or with fine, or with both.",
    "stalking": "The punishment for stalking, as per Section 354D of the Indian Penal Code (IPC), involves imprisonment which may extend to three years, and shall also be liable to fine.",
    "sexual assault": "The punishment for sexual assault, as per Section 376 of the Indian Penal Code (IPC), involves imprisonment for a term which shall not be less than seven years but which may extend to imprisonment for life, and shall also be liable to fine.",
    "crimes against children": "The punishment for crimes against children, as per the Protection of Children from Sexual Offences Act, 2012, varies depending on the specific offense but may include imprisonment and fines.",
    "terrorism": "The punishment for terrorism-related offenses, as per the Unlawful Activities (Prevention) Act, 1967, varies depending on the specific offense but may include imprisonment, fines, and in severe cases, the death penalty.",
    "insult to religion or religious beliefs": "The punishment for insult to religion or religious beliefs, as per Section 295A of the Indian Penal Code (IPC), involves imprisonment which may extend to three years, or with fine, or with both.",
    "cyberbullying": "Cyberbullying is no longer a criminal offense in India as Section 66A of the Information Technology Act, 2000, has been repealed.",
    "public nuisance": "The punishment for public nuisance, as per Section 268 of the Indian Penal Code (IPC), involves a fine not exceeding two hundred rupees.",
    "murder section 302 ipc": "The maximum punishment for murder, as per Section 302 of the Indian Penal Code (IPC), is the death penalty or life imprisonment under Section 302 IPC, along with a fine.",
    "rape section 376 ipc": "The punishment for rape, as per Section 376 of the Indian Penal Code (IPC), under Section 376 IPC, can vary depending on the circumstances, but it generally includes imprisonment for a term not less than seven years which may extend to life, along with a fine.",
    "dowry death section 304b ipc": "The punishment for dowry death, as per Section 304B of the Indian Penal Code (IPC), under Section 304B IPC, is imprisonment for a term not less than seven years which may extend to life, if it is shown that the woman died under suspicious circumstances within seven years of marriage and was subjected to cruelty or harassment by her husband or in-laws for dowry.",
    "kidnapping section 363 ipc": "The punishment for kidnapping or abduction, as per Sections 363-373 of the Indian Penal Code (IPC), under Section 363 IPC, varies depending on the circumstances and may include imprisonment which may extend to seven years and fine.",
    "theft section 378 ipc": "The punishment for theft, as per Section 378 of the Indian Penal Code (IPC), under Section 378 IPC, involves imprisonment which may extend to three years or a fine, or both.",
    "robbery section 392 ipc": "The punishment for robbery, as per Section 392 of the Indian Penal Code (IPC), under Section 392 IPC, involves imprisonment which may extend to ten years and a fine.",
    "drug trafficking narcotic drugs and psychotropic substances act": "The punishment for drug trafficking, as per the Narcotic Drugs and Psychotropic Substances Act, 1985, under the relevant sections, varies depending on the quantity and type of drug involved, but it generally involves imprisonment which may extend to rigorous imprisonment for a term not less than ten years, along with a fine."
}

constitutional_law_cases = {
    "sedition": "The punishment for sedition, as per Section 124A of the Indian Penal Code (IPC), involves imprisonment which may extend to life, along with a fine.",
    "contempt of court": "The punishment for contempt of court, as per the Contempt of Courts Act, 1971, varies depending on the specific offense but may include imprisonment which may extend to six months, or with fine, or with both. (Section 12)",
    "defamation": "The punishment for defamation, as per Section 499 of the Indian Penal Code (IPC), involves imprisonment which may extend to two years, or with fine, or with both.",
    "bribery": "The punishment for bribery, as per the Prevention of Corruption Act, 1988, involves imprisonment which shall not be less than six months but which may extend to five years, and shall also be liable to fine. (Section 7)",
    "perjury": "The punishment for perjury, as per Section 193 of the Indian Penal Code (IPC), involves imprisonment which may extend to seven years, and shall also be liable to fine.",
    "misuse of official position": "The punishment for misuse of official position, as per the Prevention of Corruption Act, 1988, involves imprisonment which shall not be less than six months but which may extend to five years, and shall also be liable to fine. (Section 13)",
    "false evidence": "The punishment for giving false evidence, as per Section 194 of the Indian Penal Code (IPC), involves imprisonment which may extend to three years, and shall also be liable to fine.",
    "corruption": "The punishment for corruption, as per the Prevention of Corruption Act, 1988, varies depending on the specific offense but may include imprisonment and fines.",
    "violating fundamental rights": "The punishment for violating fundamental rights, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court.",
    "bribery in election": "The punishment for bribery in elections, as per the Representation of the People Act, 1951, involves imprisonment which may extend to one year, or with fine, or with both. (Section 171B)",
    "violation of election code of conduct": "The punishment for violation of election code of conduct, as per the Representation of the People Act, 1951, varies depending on the specific offense but may include imprisonment, fines, and disqualification from contesting elections.",
    "interference with election process": "The punishment for interference with election process, as per the Representation of the People Act, 1951, involves imprisonment which may extend to three months, or with fine, or with both. (Section 135A)",
    "treason": "The punishment for treason, as per the Indian Penal Code (IPC) and other relevant laws, involves imprisonment which may extend to life or for a term as prescribed by law, and shall also be liable to fine.",
    "illegal detention": "The punishment for illegal detention, as per various constitutional provisions and laws, varies depending on the circumstances and may include imprisonment, fines, and other penalties as determined by the court.",
    "violation of privacy rights": "The punishment for violation of privacy rights, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court.",
    "violating freedom of speech": "The punishment for violating freedom of speech, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court.",
    "discrimination": "The punishment for discrimination, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court.",
    "violating right to equality": "The punishment for violating right to equality, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court.",
    "violating right to life": "The punishment for violating right to life, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court.",
    "violating right to education": "The punishment for violating right to education, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court. (Article 21-A, Right to Education Act)",
    "violating right to religion": "The punishment for violating right to religion, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court. (Article 25-28, Indian Constitution)",
    "violating right to property": "The punishment for violating right to property, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court. (Article 300-A, Indian Constitution)",
    "violating right to privacy": "The punishment for violating right to privacy, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court. (Article 21, Indian Constitution)",
    "violating right to freedom of religion": "The punishment for violating right to freedom of religion, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court. (Article 25-28, Indian Constitution)",
    "violating right to freedom of expression": "The punishment for violating right to freedom of expression, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court. (Article 19, Indian Constitution)",
    "violating right to liberty": "The punishment for violating right to liberty, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court. (Article 21, Indian Constitution)",
    "violating right to equality before law": "The punishment for violating right to equality before law, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court. (Article 14, Indian Constitution)",
    "violating right against exploitation": "The punishment for violating right against exploitation, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment, fines, and other penalties as determined by the court. (Article 23, Indian Constitution)",
    "violating right to constitutional remedies": "The punishment for violating right to constitutional remedies, as per various constitutional provisions and laws, varies depending on the specific violation and its consequences, but may include imprisonment."
}


civil_law_cases = {
    "breach of contract": "In case of breach of contract, the remedy would be in accordance with the terms specified in the contract itself or as per the provisions of the Indian Contract Act, 1872.",
    "trespassing": "The punishment for trespassing, as per various civil laws, may include payment of damages to the property owner, injunction orders, or eviction from the property.",
    "nuisance": "The punishment for creating a nuisance, as per various civil laws, may include injunction orders, payment of damages, or other legal remedies available to the affected party.",
    "defamation": "The punishment for defamation, as per various civil laws, may include payment of damages to the aggrieved party, injunction orders, or other legal remedies available under defamation laws.",
    "negligence": "The punishment for negligence, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under tort laws.",
    "breach of fiduciary duty": "The punishment for breach of fiduciary duty, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under trust and equity laws.",
    "fraud": "The punishment for fraud, as per various civil laws, may include payment of damages to the aggrieved party, injunction orders, or other legal remedies available under fraud laws.",
    "conversion of property": "The punishment for conversion of property, as per various civil laws, may include payment of damages to the owner of the property, injunction orders, or other legal remedies available under property laws.",
    "breach of confidentiality": "The punishment for breach of confidentiality, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under confidentiality laws.",
    "negligent misrepresentation": "The punishment for negligent misrepresentation, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under misrepresentation laws.",
    "interference with contractual relations": "The punishment for interference with contractual relations, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under contract laws.",
    "invasion of privacy": "The punishment for invasion of privacy, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under privacy laws.",
    "breach of trust": "The punishment for breach of trust, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under trust laws.",
    "interference with easement": "The punishment for interference with easement, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "wrongful termination of contract": "The punishment for wrongful termination of contract, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under contract laws.",
    "interference with right to use property": "The punishment for interference with right to use property, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "trespass to chattels": "The punishment for trespass to chattels, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "interference with trade secrets": "The punishment for interference with trade secrets, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under trade secret laws.",
    "wrongful eviction": "The punishment for wrongful eviction, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "interference with right of way": "The punishment for interference with right of way, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "violation of intellectual property rights": "The punishment for violation of intellectual property rights, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under intellectual property laws.",
    "fraudulent misrepresentation": "The punishment for fraudulent misrepresentation, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under misrepresentation laws.",
    "interference with right to water": "The punishment for interference with right to water, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under water rights laws.",
    "interference with servitudes": "The punishment for interference with servitudes, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "interference with easements": "The punishment for interference with easements, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "interference with right to light": "The punishment for interference with right to light, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "interference with right to air": "The punishment for interference with right to air, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "interference with right to support": "The punishment for interference with right to support, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws.",
    "violation of zoning laws": "The punishment for violation of zoning laws, as per various civil laws, may include payment of fines, injunction orders, or other legal remedies available under zoning laws.",
    "interference with right to passage": "The punishment for interference with right to passage, as per various civil laws, may include payment of damages to the affected party, injunction orders, or other legal remedies available under property laws."
}


family_law_cases = {
    "domestic violence": "The punishment for domestic violence, as per Section 31 of the Protection of Women from Domestic Violence Act, 2005, may include imprisonment which may extend to three years, and also be liable to fine.",
    "child marriage": "The punishment for child marriage, as per Section 9 of the Prohibition of Child Marriage Act, 2006, may include imprisonment which may extend to two years, or with fine, or both.",
    "dowry harassment": "The punishment for dowry harassment, as per Section 4 of the Dowry Prohibition Act, 1961, may include imprisonment which may extend to five years, and shall also be liable to fine.",
    "bigamy": "The punishment for bigamy, as per Section 494 of the Indian Penal Code (IPC), may include imprisonment which may extend to seven years, and shall also be liable to fine.",
    "adultery": "The punishment for adultery, as per Section 497 of the Indian Penal Code (IPC), may include imprisonment which may extend to five years, or with fine, or with both.",
    "child custody": "There is no specific punishment associated with child custody matters. The award of child custody is determined by the court based on various factors including the welfare of the child.",
    "parental kidnapping": "The punishment for parental kidnapping may be determined under various sections of the Indian Penal Code (IPC) depending on the circumstances.",
    "child neglect": "The punishment for child neglect, as per Section 75 of the Juvenile Justice (Care and Protection of Children) Act, 2015, may include imprisonment which may extend to six months, or with fine, or with both.",
    "maintenance of parents": "The punishment for failure to maintain parents, as per Section 24 of the Maintenance and Welfare of Parents and Senior Citizens Act, 2007, may include imprisonment which may extend to three months, or with fine, or with both.",
    "adoption": "There is no specific punishment associated with adoption. The process of adoption is governed by the relevant adoption laws such as the Hindu Adoption and Maintenance Act, 1956.",
    "surrogacy": "There is no specific punishment associated with surrogacy. The regulation of surrogacy is governed by the relevant laws such as the Surrogacy (Regulation) Bill, 2019.",
    "alimony": "There is no specific punishment associated with alimony or maintenance orders. The award of alimony or maintenance is determined by the court based on various factors such as the financial situation of the parties involved.",
    "annulment of marriage": "There is no specific punishment associated with annulment of marriage. The annulment of marriage is determined by the court based on various grounds specified under the personal laws applicable to the parties involved.",
    "survivorship rights": "There is no specific punishment associated with survivorship rights. The survivorship rights are determined by the relevant laws governing inheritance and succession.",
    "partition of property": "There is no specific punishment associated with partition of property. The partition of property is determined by the court based on various factors including the rights of the co-owners.",
    "domestic partnership": "There is no specific punishment associated with domestic partnerships. The rights and obligations in a domestic partnership are determined by the relevant laws governing domestic relationships.",
    "spousal support": "There is no specific punishment associated with spousal support. The award of spousal support is determined by the court based on various factors including the financial situation of the parties involved.",
    "parental rights": "There is no specific punishment associated with parental rights. The determination of parental rights is governed by the relevant laws governing parental responsibilities.",
    "guardianship of minor": "There is no specific punishment associated with guardianship of a minor. The appointment of guardianship of a minor is determined by the court based on the welfare of the child.",
    "division of assets after divorce": "There is no specific punishment associated with division of assets after divorce. The division of assets after divorce is determined by the court based on various factors including the financial situation of the parties involved.",
    "inheritance disputes": "There is no specific punishment associated with inheritance disputes. The resolution of inheritance disputes is determined by the court based on the relevant laws such as the Indian Succession Act, 1925.",
    "paternity disputes": "There is no specific punishment associated with paternity disputes. The resolution of paternity disputes is determined by the court based on various factors including DNA testing.",
    "custody of minor": "There is no specific punishment associated with custody of a minor. The award of custody of a minor is determined by the court based on the welfare of the child.",
    "property settlement after divorce": "There is no specific punishment associated with property settlement after divorce. The settlement of property after divorce is determined by the court based on various factors including the financial situation of the parties involved.",
    "interference with visitation rights": "There is no specific punishment associated with interference with visitation rights. The interference with visitation rights may lead to legal actions such as contempt of court proceedings.",
    "breach of matrimonial duties": "There is no specific punishment associated with breach of matrimonial duties. The breach of matrimonial duties may lead to legal actions such as divorce proceedings.",
    "failure to pay child support": "The punishment for failure to pay child support, as per Section 125 of the Code of Criminal Procedure, 1973, may include imprisonment which may extend to one month, or with fine, or with both.",
    "refusal to grant divorce": "There is no specific punishment associated with refusal to grant divorce. The refusal to grant divorce may lead to legal actions such as contested divorce proceedings.",
    "interference with parental rights": "There is no specific punishment associated with interference with parental rights. The interference with parental rights may lead to legal actions such as contempt of court proceedings.",
    "violation of child custody order": "The punishment for violation of child custody order may be determined under various sections of the Indian Penal Code (IPC) depending on the circumstances.",
    "denial of conjugal rights": "There is no specific punishment associated with denial of conjugal rights. The denial of conjugal rights may lead to legal actions such as divorce proceedings.",
    "remarriage during subsistence of marriage": "The punishment for remarriage during subsistence of marriage, as per Section 494 of the Indian Penal Code (IPC), may include imprisonment which may extend to seven years, and shall also be liable to fine.",
    "failure to pay alimony": "There is no specific punishment associated with failure to pay alimony or maintenance. The failure to pay alimony or maintenance may lead to legal actions such as contempt of court proceedings.",
    "interference with matrimonial home": "There is no specific punishment associated with interference with matrimonial home. The interference with matrimonial home may lead to legal actions such as eviction proceedings.",
    "interference with adoption process": "The punishment for interference with adoption process may be determined under various sections of the relevant adoption laws depending on the circumstances."
}


commercial_law_cases = {
    "counterfeiting": "The punishment for counterfeiting, as per Section 28 of the Trademarks Act, 1999, involves imprisonment which may extend to three years, or with fine, or with both.",
    "copyright infringement": "The punishment for copyright infringement, as per Section 63 of the Copyright Act, 1957, involves imprisonment which may extend to three years, or with fine, or with both.",
    "patent violation": "The punishment for patent violation, as per Section 118 of the Patents Act, 1970, involves imprisonment which may extend to two years, or with fine, or with both.",
    "trademark infringement": "The punishment for trademark infringement, as per Section 103 of the Trademarks Act, 1999, involves imprisonment which may extend to three years, or with fine, or with both.",
    "insurance fraud": "The punishment for insurance fraud, as per Section 41 of the Insurance Act, 1938, involves imprisonment which may extend to three years, or with fine, or with both.",
    "bank fraud": "The punishment for bank fraud, as per Section 65 of the Banking Regulation Act, 1949, involves imprisonment which may extend to ten years, or with fine, or with both.",
    "embezzlement": "The punishment for embezzlement, as per Section 403 of the Indian Penal Code (IPC), involves imprisonment which may extend to seven years, or with fine, or with both.",
    "money laundering": "The punishment for money laundering, as per the Prevention of Money Laundering Act, 2002, involves imprisonment which may extend to three years, or with fine, or with both.",
    "insider trading": "The punishment for insider trading, as per the Securities and Exchange Board of India (SEBI) Act, 1992, involves imprisonment which may extend to ten years, or with fine, or with both.",
    "fraudulent misrepresentation": "The punishment for fraudulent misrepresentation, as per Section 447 of the Companies Act, 2013, involves imprisonment which may extend to two years, or with fine, or with both.",
    "cartelization": "The punishment for cartelization, as per Section 3 of the Competition Act, 2002, involves imprisonment which may extend to three years, or with fine, or with both.",
    "insolvency fraud": "The punishment for insolvency fraud, as per Section 216 of the Insolvency and Bankruptcy Code, 2016, involves imprisonment which may extend to five years, or with fine, or with both.",
    "tax evasion": "The punishment for tax evasion, as per Section 276C of the Income Tax Act, 1961, involves imprisonment which may extend to seven years, or with fine, or with both.",
    "bribery in business transactions": "The punishment for bribery in business transactions, as per Section 9 of the Prevention of Corruption Act, 1988, involves imprisonment which shall not be less than three years but which may extend to seven years, and shall also be liable to fine.",
    "fraudulent conveyance": "The punishment for fraudulent conveyance, as per Section 53 of the Transfer of Property Act, 1882, involves imprisonment which may extend to three months, or with fine, or with both.",
    "forgery": "The punishment for forgery, as per Section 463 of the Indian Penal Code (IPC), involves imprisonment which may extend to two years, or with fine, or with both.",
    "cybercrime": "The punishment for cybercrime, as per the Information Technology (IT) Act, 2000, varies depending on the specific offense but may include imprisonment and fines.",
    "consumer fraud": "The punishment for consumer fraud, as per the Consumer Protection Act, 2019, involves imprisonment which may extend to five years, or with fine, or with both.",
    "misrepresentation of financial statements": "The punishment for misrepresentation of financial statements, as per Section 447 of the Companies Act, 2013, involves imprisonment which may extend to two years, or with fine, or with both.",
    "price fixing": "The punishment for price fixing, as per Section 3 of the Competition Act, 2002, involves imprisonment which may extend to three years, or with fine, or with both.",
    "stock market manipulation": "The punishment for stock market manipulation, as per the Securities and Exchange Board of India (SEBI) Act, 1992, involves imprisonment which may extend to ten years, or with fine, or with both.",
    "fraudulent advertising": "The punishment for fraudulent advertising, as per the Consumer Protection Act, 2019, involves imprisonment which may extend to two years, or with fine, or with both.",
    "violation of contract terms": "The punishment for violation of contract terms may vary depending on the specific contractual terms and the legal provisions applicable to the contract.",
    "dumping": "The punishment for dumping, as per Section 9A of the Customs Tariff Act, 1975, involves imprisonment which may extend to five years, or with fine, or with both.",
    "tax fraud": "The punishment for tax fraud, as per Section 276C of the Income Tax Act, 1961, involves imprisonment which may extend to seven years, or with fine, or with both.",
    "kickbacks": "The punishment for kickbacks, as per Section 8 of the Prevention of Corruption Act, 1988, involves imprisonment which shall not be less than three years but which may extend to seven years, and shall also be liable to fine.",
    "bid rigging": "The punishment for bid rigging, as per Section 3 of the Competition Act, 2002, involves imprisonment which may extend to three years, or with fine, or with both.",
    "corporate espionage": "The punishment for corporate espionage, as per Section 408 of the Indian Penal Code (IPC), involves imprisonment which may extend to seven years, or with fine, or with both.",
    "trade secret theft": "The punishment for trade secret theft may vary depending on the legal provisions applicable to intellectual property rights and trade secrets."
}

labour_employment_law_cases = {
   "minimum wage violation": "The punishment for minimum wage violation, as per the Minimum Wages Act, 1948, involves imprisonment which may extend to six months, or with fine, or with both. (Section 22)",
    "child labor": "The punishment for employing child labor, as per the Child Labour (Prohibition and Regulation) Act, 1986, involves imprisonment which may extend to two years, or with fine, or with both. (Section 14)",
    "bonded labor": "The punishment for bonded labor, as per the Bonded Labour System (Abolition) Act, 1976, involves imprisonment which may extend to three years, or with fine, or with both. (Section 16)",
    "sexual harassment at workplace": "The punishment for sexual harassment at the workplace, as per the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013, involves imprisonment which may extend to three years, or with fine, or with both. (Section 509 IPC)",
    "discrimination in employment": "The punishment for discrimination in employment, as per the Equal Remuneration Act, 1976, involves imprisonment which may extend to one year, or with fine, or with both. (Section 7)",
    "failure to provide Provident Fund": "The punishment for failure to provide Provident Fund, as per the Employees' Provident Funds and Miscellaneous Provisions Act, 1952, involves imprisonment which may extend to one year, or with fine, or with both. (Section 14B)",
    "violation of Maternity Benefit Act": "The punishment for violation of the Maternity Benefit Act, 1961, involves imprisonment which may extend to three months, or with fine, or with both. (Section 21)",
    "unfair dismissal": "The punishment for unfair dismissal, as per the Industrial Disputes Act, 1947, involves reinstatement of the employee with back wages or compensation. (Section 11A)",
    "violation of Industrial Employment (Standing Orders) Act": "The punishment for violation of the Industrial Employment (Standing Orders) Act, 1946, involves imprisonment which may extend to six months, or with fine, or with both. (Section 26)",
    "violating Occupational Safety and Health standards": "The punishment for violating Occupational Safety and Health standards, as per the Factories Act, 1948, involves imprisonment which may extend to two years, or with fine, or with both. (Section 92)",
    "violation of Contract Labour Act": "The punishment for violation of the Contract Labour (Regulation and Abolition) Act, 1970, involves imprisonment which may extend to three months, or with fine, or with both. (Section 21)",
    "non-compliance with Payment of Bonus Act": "The punishment for non-compliance with the Payment of Bonus Act, 1965, involves imprisonment which may extend to six months, or with fine, or with both. (Section 28)",
    "violation of Employees' State Insurance Act": "The punishment for violation of the Employees' State Insurance Act, 1948, involves imprisonment which may extend to two years, or with fine, or with both. (Section 85)",
    "violation of Employees' Compensation Act": "The punishment for violation of the Employees' Compensation Act, 1923, involves imprisonment which may extend to one year, or with fine, or with both. (Section 28)",
    "failure to provide Gratuity": "The punishment for failure to provide Gratuity, as per the Payment of Gratuity Act, 1972, involves imprisonment which may extend to six months, or with fine, or with both. (Section 9)",
    "employment of foreign nationals without valid work permit": "The punishment for employment of foreign nationals without a valid work permit may vary depending on the immigration laws and regulations applicable in the country.",
    "violation of Apprentices Act": "The punishment for violation of the Apprentices Act, 1961, involves imprisonment which may extend to six months, or with fine, or with both. (Section 30)",
    "non-compliance with Payment of Wages Act": "The punishment for non-compliance with the Payment of Wages Act, 1936, involves imprisonment which may extend to six months, or with fine, or with both. (Section 20)",
    "violation of Shops and Establishments Act": "The punishment for violation of the Shops and Establishments Act may vary depending on the specific provisions of the respective state's Act.",
    "non-compliance with Labour Welfare Fund Act": "The punishment for non-compliance with the Labour Welfare Fund Act may vary depending on the specific provisions of the respective state's Act.",
    "violation of Industrial Relations Code": "The punishment for violation of the Industrial Relations Code, 2020, involves penalties as prescribed under the relevant sections of the Code.",
    "non-compliance with Equal Remuneration Act": "The punishment for non-compliance with the Equal Remuneration Act, 1976, involves imprisonment which may extend to one year, or with fine, or with both. (Section 12)",
    "violation of Payment of Gratuity Act": "The punishment for violation of the Payment of Gratuity Act, 1972, involves imprisonment which may extend to six months, or with fine, or with both. (Section 9)",
    "violation of Factories Act": "The punishment for violation of the Factories Act, 1948, involves imprisonment which may extend to two years, or with fine, or with both. (Section 92)",
    "non-compliance with Contract Labour Act": "The punishment for non-compliance with the Contract Labour (Regulation and Abolition) Act, 1970, involves imprisonment which may extend to three months, or with fine, or with both. (Section 21)",
    "failure to provide safe working conditions": "The punishment for failure to provide safe working conditions, as per the Occupational Safety, Health and Working Conditions Code, 2020, involves penalties as prescribed under the relevant sections of the Code.",
    "non-compliance with Employees' Provident Funds Act": "The punishment for non-compliance with the Employees' Provident Funds and Miscellaneous Provisions Act, 1952, involves imprisonment which may extend to one year, or with fine, or with both. (Section 14B)",
    "violation of Payment of Bonus Act": "The punishment for violation of the Payment of Bonus Act, 1965, involves imprisonment which may extend to six months, or with fine, or with both. (Section 28)",
    "failure to provide employee benefits": "The punishment for failure to provide employee benefits may vary depending on the specific provisions of the relevant labor laws and regulations.",
    "non-compliance with Industrial Disputes Act": "The punishment for non-compliance with the Industrial Disputes Act, 1947, involves penalties as prescribed under the relevant sections of the Act."
}

cyber_law_cases = {
    "hacking": "The punishment for hacking, as per Section 66 of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine which may extend to five lakh rupees, or with both.",
    "identity theft": "The punishment for identity theft, as per Section 66C of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine which may extend to five lakh rupees, or with both.",
    "online fraud": "The punishment for online fraud, as per Section 66D of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine which may extend to five lakh rupees, or with both.",
    "cyber stalking": "The punishment for cyber stalking, as per Section 354D of the Indian Penal Code (IPC), involves imprisonment which may extend to three years, or with fine, or with both.",
    "phishing": "The punishment for phishing, as per Section 66C of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine which may extend to five lakh rupees, or with both.",
    "cyberbullying": "The punishment for cyberbullying, as per Section 66A of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine.",
    "data theft": "The punishment for data theft, as per Section 43 of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine which may extend to five lakh rupees, or with both.",
    "cyber terrorism": "The punishment for cyber terrorism, as per Section 66F of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to imprisonment for life.",
    "online piracy": "The punishment for online piracy, as per Section 63 of the Copyright Act, 1957, involves imprisonment which may extend to three years, or with fine which may extend to two lakh rupees, or with both.",
    "cyber squatting": "The punishment for cyber squatting, as per Section 43(d) of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to two years, or with fine which may extend to one lakh rupees, or with both.",
    "copyright infringement online": "The punishment for copyright infringement online, as per Section 63 of the Copyright Act, 1957, involves imprisonment which may extend to three years, or with fine which may extend to two lakh rupees, or with both.",
    "online harassment": "The punishment for online harassment, as per Section 66A of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine.",
    "cyber espionage": "The punishment for cyber espionage, as per Section 66C of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine which may extend to five lakh rupees, or with both.",
    "unauthorized access to computer systems": "The punishment for unauthorized access to computer systems, as per Section 66 of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine which may extend to five lakh rupees, or with both.",
    "computer virus dissemination": "The punishment for computer virus dissemination, as per Section 43 of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine which may extend to five lakh rupees, or with both.",
    "online defamation": "The punishment for online defamation, as per Section 66A of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine.",
    "cyber extortion": "The punishment for cyber extortion, as per Section 66E of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years, or with fine which may extend to two lakh rupees, or with both.",
    "spoofing": "The punishment for spoofing, as per Section 66C of the Information Technology (IT) Act, 2000, involves imprisonment which may extend to three years."
}

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return None

def query_law_cases(query):
    if query in civil_law_cases:
        return civil_law_cases[query]
    elif query in constitutional_law_cases:
        return constitutional_law_cases[query]
    elif query in general_crime_cases:
        return general_crime_cases[query]
    elif query in family_law_cases:
        return family_law_cases[query]
    elif query in commercial_law_cases:
        return commercial_law_cases[query]
    elif query in labour_employment_law_cases:
        return labour_employment_law_cases[query]
    elif query in cyber_law_cases:
        return cyber_law_cases[query]
    else:
        return "No information available for the given query."
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    bot_response = query_law_cases(user_message)
    return render_template('index.html', user_message=user_message, bot_response=bot_response)

@app.route('/voice_chat', methods=['POST'])
def voice_chat():
    query =get_audio()
    if query:
        bot_response = query_law_cases(query)
        speak(bot_response)
    else:
        bot_response = "Sorry, I didn't catch that. Could you please repeat?"
    return render_template('index.html', user_message=query, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

def main():
    print("Enter your query: (or type 'hi bot' to activate voice search)")
    while True:
        user_input = input().lower()
        if user_input == "hi bot":
            query = get_audio()
            if query:
                response = query_law_cases(query)
                print(response)
                speak(response)
        elif "thank you" in user_input:
            print("You're welcome, visit us again!")
            speak("You're welcome, visit us again!")
        else:
            response = query_law_cases(user_input)
            print(response)
            speak(response)

if __name__ == "__main__":
    main()

