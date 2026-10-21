"""Génère deux FEC fictifs (2024 et 2025) d'une PME de menuiserie, avec des anomalies connues en 2025."""
import calendar, datetime as dt, os, random, sys
from collections import defaultdict

OUT = sys.argv[1]
SIREN = "999000111"
random.seed(42)

COLS = ['JournalCode', 'JournalLib', 'EcritureNum', 'EcritureDate', 'CompteNum', 'CompteLib', 'CompAuxNum', 'CompAuxLib',
        'PieceRef', 'PieceDate', 'EcritureLib', 'Debit', 'Credit', 'EcritureLet', 'DateLet', 'ValidDate', 'Montantdevise', 'Idevise']

JOURNAUX = {'AN': 'A-nouveaux', 'VT': 'Journal des ventes', 'AC': 'Journal des achats',
            'BQ': 'Banque Fictive', 'OD': 'Operations diverses', 'SA': 'Salaires', 'INV': 'Inventaire'}

COMPTES = {
    '101300': 'Capital souscrit appele verse', '106100': 'Reserve legale', '110000': 'Report a nouveau',
    '120000': "Resultat de l'exercice", '164000': 'Emprunts aupres des etablissements de credit',
    '215400': 'Materiel industriel', '218300': 'Materiel de bureau et informatique',
    '281540': 'Amortissements materiel industriel', '281830': 'Amortissements materiel de bureau',
    '310000': 'Stocks de matieres premieres', '401000': 'Fournisseurs', '411000': 'Clients',
    '421000': 'Personnel remunerations dues', '431000': 'Securite sociale', '444000': 'Etat impot sur les benefices',
    '445510': 'TVA a decaisser', '445660': 'TVA deductible sur ABS', '445670': 'Credit de TVA a reporter',
    '445710': 'TVA collectee', '455100': "Compte courant d'associe", '512000': 'Banque Fictive',
    '601000': 'Achats de matieres premieres', '603100': 'Variation des stocks de matieres premieres',
    '606100': 'Fournitures non stockables energie', '613200': 'Locations immobilieres', '616000': "Primes d'assurance",
    '622600': 'Honoraires', '625100': 'Voyages et deplacements', '626000': 'Frais postaux et telecommunications',
    '627000': 'Services bancaires', '635110': 'Cotisation fonciere des entreprises', '641000': 'Remunerations du personnel',
    '645100': 'Cotisations URSSAF', '661100': 'Interets des emprunts', '681120': 'Dotations aux amortissements des immobilisations corporelles',
    '695000': 'Impots sur les benefices', '701000': 'Ventes de produits finis',
}

CLIENTS = {'C001': 'Hotel Les Tilleuls', 'C002': 'Agence Mobilis', 'C003': 'Residence Bel Air', 'C004': 'Cabinet Varenne Associes',
           'C005': 'Restaurant Le Comptoir', 'C006': 'Clinique du Parc', 'C007': 'Boutique Hetre et Chene', 'C008': 'Coworking Atelier 9'}
FOURN = {'F001': 'Scierie du Nord', 'F002': 'Quincaillerie Pro Est', 'F003': 'Vernis et Finitions', 'F004': 'SCI Les Halles',
         'F005': 'Energie Plus', 'F006': 'Assurances Mutuelles Exemple', 'F007': 'Cabinet Comptable Exemple', 'F008': 'Telecom Pro'}


def d2s(d): return d.strftime('%Y%m%d')
def amt(x): return f"{x:.2f}".replace('.', ',') if x else '0,00'
def r2(x): return round(x + 1e-9, 2)
def eom(y, m): return dt.date(y, m, calendar.monthrange(y, m)[1])
def bday(y, m, lo=1, hi=None):
    hi = hi or calendar.monthrange(y, m)[1]
    while True:
        d = dt.date(y, m, random.randint(lo, hi))
        if d.weekday() < 5: return d


class Exercice:
    def __init__(self, year):
        self.year = year
        self.entries = []          # chaque écriture : dict(jc, date, piece, lib, lines=[...])
        self.num = defaultdict(int)
        self.letters = 0

    def add(self, jc, date, piece, lib, lines):
        """lines : (compte, aux, debit, credit[, cle_lettrage])"""
        self.num[jc] += 1
        e = dict(jc=jc, date=date, piece=piece, lib=lib, num=f"{jc}{self.num[jc]:05d}", lines=[])
        for ln in lines:
            acct, aux, d, c = ln[:4]
            e['lines'].append(dict(acct=acct, aux=aux, d=r2(d), c=r2(c), key=ln[4] if len(ln) > 4 else None, let='', dlet=None))
        self.entries.append(e)
        return e

    def next_letter(self):
        self.letters += 1
        n, s = self.letters, ''
        while n: n, r = divmod(n - 1, 26); s = chr(65 + r) + s
        return s.rjust(3, 'A')

    def write(self, path):
        rows = ['\t'.join(COLS)]
        for e in sorted(self.entries, key=lambda e: (e['date'], e['jc'], e['num'])):
            vd = e['date'] + dt.timedelta(days=random.randint(2, 20))
            vd = min(vd, dt.date(self.year + 1, 3, 31))
            for l in e['lines']:
                aux = l['aux'] or ''
                auxlib = CLIENTS.get(aux) or FOURN.get(aux) or ''
                rows.append('\t'.join([e['jc'], JOURNAUX[e['jc']], e['num'], d2s(e['date']), l['acct'], COMPTES[l['acct']], aux, auxlib,
                                       e['piece'], d2s(e['date']), e['lib'], amt(l['d']), amt(l['c']), l['let'],
                                       d2s(l['dlet']) if l['dlet'] else '', d2s(vd), '', '']))
        with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write('\n'.join(rows) + '\n')

    def balances(self):
        b = defaultdict(float)
        for e in self.entries:
            for l in e['lines']: b[l['acct']] += l['d'] - l['c']
        return b


def letter(ex, line_a, line_b, date):
    code = ex.next_letter()
    for l in (line_a, line_b): l['let'], l['dlet'] = code, date


def run_year(ex, opening, params, carry):
    """opening : lignes d'à-nouveaux ; carry : postes ouverts reportés {('411'|'401', aux, piece): (ligne AN, montant, echeance)}"""
    y = ex.year
    an = ex.add('AN', dt.date(y, 1, 1), f'AN{y}', f'A-nouveaux {y}', opening)
    # postes ouverts issus des à-nouveaux (ligne AN = clé)
    open_cli, open_fou = [], []
    for l in an['lines']:
        if l['key']:
            kind, due = l['key']
            (open_cli if kind == 'C' else open_fou).append((l, due))
    pending_payments = []   # (date, type, ...)
    tva = defaultdict(lambda: [0.0, 0.0])   # mois -> [collectee, deductible]
    inv = 0
    gross = params['salaires']
    unpaid_urssaf = params.get('urssaf_impayes', set())
    loan = carry['emprunt']

    for m in range(1, 13):
        # ------------------------------------------------ ventes
        n_inv = random.randint(4, 6)
        ca_m = params['ca'][m - 1]
        parts = [random.uniform(0.6, 1.4) for _ in range(n_inv)]
        for p in parts:
            ht = r2(ca_m * p / sum(parts)); tv = r2(ht * 0.2); ttc = r2(ht + tv)
            cli = random.choice(list(CLIENTS))
            d = bday(y, m); inv += 1; piece = f"FA{y}-{inv:04d}"
            e = ex.add('VT', d, piece, f"Facture {piece} {CLIENTS[cli]}", [('411000', cli, ttc, 0), ('701000', None, 0, ht), ('445710', None, 0, tv)])
            tva[m][0] += tv
            pay = d + dt.timedelta(days=random.randint(*params['delai_clients']))
            open_cli.append((e['lines'][0], pay))
        # ------------------------------------------------ achats matières
        mat_m = ca_m * params['taux_matieres']
        wts = [random.uniform(0.7, 1.3) for _ in range(random.randint(2, 3))]
        for i, w in enumerate(wts):
            ht = r2(mat_m * w / sum(wts)); tv = r2(ht * 0.2)
            f = random.choice(['F001', 'F001', 'F002', 'F003'])
            d = dt.date(y, 12, 29) if (m == 12 and i == 0) else bday(y, m); piece = f"{f}-{y}{m:02d}{i + 1}"
            e = ex.add('AC', d, piece, f"Facture {FOURN[f]} {piece}", [('601000', None, ht, 0), ('445660', None, tv, 0), ('401000', f, 0, r2(ht + tv))])
            tva[m][1] += tv
            open_fou.append((e['lines'][2], d + dt.timedelta(days=random.randint(*params['delai_fourn']))))
        # ------------------------------------------------ frais généraux
        frais = [('F004', '613200', 8500), ('F005', '606100', r2(3000 * random.uniform(0.8, 1.25))), ('F008', '626000', 480)]
        if m in (1, 4, 7, 10): frais.append(('F006', '616000', 3000))
        if m % 3 == 0: frais.append(('F007', '622600', 6000))
        for f, acct, ht in frais:
            tv = 0 if acct == '616000' else r2(ht * 0.2)
            d = dt.date(y, m, 5); piece = f"{f}-{y}{m:02d}"
            lines = [(acct, None, ht, 0)] + ([('445660', None, tv, 0)] if tv else []) + [('401000', f, 0, r2(ht + tv))]
            e = ex.add('AC', d, piece, f"Facture {FOURN[f]} {y}-{m:02d}", lines)
            tva[m][1] += tv
            open_fou.append((e['lines'][-1], d + dt.timedelta(days=30)))
        # ------------------------------------------------ paie
        g = r2(gross * random.uniform(0.98, 1.02)); pat = r2(g * 0.42); sal = r2(g * 0.22); net = r2(g - sal)
        ex.add('SA', eom(y, m), f"PAIE{y}{m:02d}", f"Paie {m:02d}/{y}", [('641000', None, g, 0), ('645100', None, pat, 0), ('421000', None, 0, net), ('431000', None, 0, r2(sal + pat))])
        ex.add('BQ', eom(y, m), f"VIRSAL{y}{m:02d}", f"Virement salaires {m:02d}/{y}", [('421000', None, net, 0), ('512000', None, 0, net)])
        if m < 12 and m not in unpaid_urssaf:
            pending_payments.append((dt.date(y, m + 1, 15), 'urssaf', r2(sal + pat), m))
        if m == 12:
            carry['urssaf_dec'] = r2(sal + pat)
        # ------------------------------------------------ banque : emprunt, frais
        it = r2(loan * 0.04 / 12); loan = r2(loan - 2000)
        ex.add('BQ', dt.date(y, m, 10), f"ECH{y}{m:02d}", f"Echeance emprunt {m:02d}/{y}", [('164000', None, 2000, 0), ('661100', None, it, 0), ('512000', None, 0, r2(2000 + it))])
        ex.add('BQ', eom(y, m), f"FRB{y}{m:02d}", f"Frais bancaires {m:02d}/{y}", [('627000', None, 85, 0), ('512000', None, 0, 85)])
        # ------------------------------------------------ TVA du mois
        col, ded = r2(tva[m][0]), r2(tva[m][1]); net_tva = r2(col - ded)
        lines = [('445710', None, col, 0), ('445660', None, 0, ded)]
        lines.append(('445510', None, 0, net_tva) if net_tva >= 0 else ('445670', None, -net_tva, 0))
        ex.add('OD', eom(y, m), f"CA3-{y}{m:02d}", f"Declaration TVA {m:02d}/{y}", lines)
        if net_tva > 0:
            if m < 12: pending_payments.append((dt.date(y, m + 1, 20), 'tva', net_tva, m))
            else: carry['tva_dec'] = net_tva

    # ------------------------------------------------ paiements reportés de l'exercice précédent (URSSAF, TVA, IS de décembre)
    for kind, label, acct in (('urssaf_prev', 'URSSAF', '431000'), ('tva_prev', 'TVA', '445510')):
        if carry.get(kind):
            day = 15 if acct == '431000' else 20
            ex.add('BQ', dt.date(y, 1, day), f"{label}{y - 1}12", f"Reglement {label} 12/{y - 1}", [(acct, None, carry[kind], 0), ('512000', None, 0, carry[kind])])
    if carry.get('is_prev'):
        ex.add('BQ', dt.date(y, 4, 15), f"IS{y - 1}", f"Solde IS {y - 1}", [('444000', None, carry['is_prev'], 0), ('512000', None, 0, carry['is_prev'])])
    for d, kind, v, m in pending_payments:
        acct, label = ('431000', 'URSSAF') if kind == 'urssaf' else ('445510', 'TVA')
        ex.add('BQ', d, f"{label}{y}{m:02d}", f"Reglement {label} {m:02d}/{y}", [(acct, None, v, 0), ('512000', None, 0, v)])

    # ------------------------------------------------ hooks propres à l'exercice (anomalies, apports...)
    for hook in params.get('hooks', []):
        hook(ex, open_cli, open_fou)

    # ------------------------------------------------ encaissements et décaissements, avec lettrage
    end = dt.date(y, 12, 31)
    still_cli, still_fou = [], []
    for l, due in open_cli:
        if due <= end and l.get('never') is not True:
            while due.weekday() >= 5: due += dt.timedelta(days=1)
            if due > end: still_cli.append((l, due)); continue
            v = r2(l['d'] - l['c'])
            e = ex.add('BQ', due, f"ENC-{l['_piece']}", f"Reglement client {CLIENTS[l['aux']]} {l['_piece']}", [('512000', None, v, 0), ('411000', l['aux'], 0, v)])
            letter(ex, l, e['lines'][1], due)
        else:
            still_cli.append((l, due))
    for l, due in open_fou:
        if due <= end and l.get('never') is not True:
            while due.weekday() >= 5: due += dt.timedelta(days=1)
            if due > end: still_fou.append((l, due)); continue
            v = r2(l['c'] - l['d'])
            e = ex.add('BQ', due, f"DEC-{l['_piece']}", f"Reglement fournisseur {FOURN[l['aux']]} {l['_piece']}", [('401000', l['aux'], v, 0), ('512000', None, 0, v)])
            letter(ex, l, e['lines'][0], due)
        else:
            still_fou.append((l, due))

    # ------------------------------------------------ CFE, inventaire, amortissements
    ex.add('BQ', dt.date(y, 12, 15), f"CFE{y}", f"CFE {y}", [('635110', None, 4500, 0), ('512000', None, 0, 4500)])
    s0, s1 = carry['stock'], params['stock_final']
    ex.add('INV', end, f"INV{y}-1", f"Annulation stock initial {y}", [('603100', None, s0, 0), ('310000', None, 0, s0)])
    ex.add('INV', end, f"INV{y}-2", f"Stock final au 31/12/{y}", [('310000', None, s1, 0), ('603100', None, 0, s1)])
    ex.add('OD', end, f"DAP{y}", f"Dotations aux amortissements {y}", [('681120', None, 23000, 0), ('281540', None, 0, 18000), ('281830', None, 0, 5000)])
    # IS : 15 % du bénéfice, rien en cas de perte
    b = ex.balances(); res = -sum(v for k, v in b.items() if k[0] in '67')
    is_ = r2(max(0, res) * 0.15)
    if is_:
        ex.add('OD', end, f"IS{y}", f"Impot sur les societes {y}", [('695000', None, is_, 0), ('444000', None, 0, is_)])
    carry.update(stock=s1, emprunt=loan, urssaf_prev=carry.get('urssaf_dec'), tva_prev=carry.get('tva_dec'), is_prev=is_ or None,
                 urssaf_dec=None, tva_dec=None)
    return still_cli, still_fou


def tag_pieces(ex):
    for e in ex.entries:
        for l in e['lines']: l.setdefault('_piece', e['piece'])


# Les lignes de tiers doivent connaître leur pièce : on l'injecte au fil de l'eau
_orig_add = Exercice.add
def _add(self, *a, **k):
    e = _orig_add(self, *a, **k)
    for l in e['lines']: l['_piece'] = e['piece']
    return e
Exercice.add = _add


def opening_from(prev, still_cli, still_fou):
    """À-nouveaux de l'exercice suivant : soldes des classes 1 à 5, tiers détaillés par poste ouvert, résultat en 120."""
    b = prev.balances()
    res = -sum(v for k, v in b.items() if k[0] in '67')
    lines = []
    for acct in sorted(b):
        if acct[0] not in '12345' or acct in ('411000', '401000') or abs(b[acct]) < 0.005: continue
        v = r2(b[acct]); lines.append((acct, None, v if v > 0 else 0, -v if v < 0 else 0))
    lines.append(('120000', None, 0 if res > 0 else r2(-res), r2(res) if res > 0 else 0))
    for l, due in still_cli:
        lines.append(('411000', l['aux'], r2(l['d'] - l['c']), 0, ('C', due)))
    for l, due in still_fou:
        lines.append(('401000', l['aux'], 0, r2(l['c'] - l['d']), ('F', due)))
    return lines, res


# ====================================================================== 2024
opening24 = [
    ('101300', None, 0, 100000), ('106100', None, 0, 10000), ('110000', None, 0, 68000), ('164000', None, 0, 90000),
    ('215400', None, 180000, 0), ('218300', None, 25000, 0), ('281540', None, 0, 70000), ('281830', None, 0, 12000),
    ('310000', None, 45000, 0), ('512000', None, 85000, 0), ('455100', None, 0, 15000),
    ('431000', None, 0, 18000), ('445510', None, 0, 12000),
]
cli23 = [('C001', 30000), ('C003', 26000), ('C004', 22000), ('C006', 24000), ('C008', 18000)]
for i, (c, v) in enumerate(cli23):
    opening24.append(('411000', c, v, 0, ('C', dt.date(2024, 1, 15 + 3 * i))))
for i, (f, v) in enumerate([('F001', 28000), ('F002', 12000), ('F003', 9000), ('F005', 4000), ('F004', 7000)]):
    opening24.append(('401000', f, 0, v, ('F', dt.date(2024, 1, 10 + 4 * i))))

ca24 = [r2(2000000 / 12 * s) for s in (0.85, 0.9, 1.05, 1.05, 1.1, 1.1, 0.95, 0.7, 1.05, 1.1, 1.1, 0.95)]
ex24 = Exercice(2024)
carry = dict(stock=45000, emprunt=90000, urssaf_prev=None, tva_prev=None, is_prev=None)
# Les dettes URSSAF et TVA des à-nouveaux 2024 se règlent en janvier
carry['urssaf_prev'], carry['tva_prev'] = 18000, 12000
p24 = dict(ca=ca24, taux_matieres=0.42, salaires=52000, delai_clients=(25, 50), delai_fourn=(45, 60), stock_final=52000)
sc24, sf24 = run_year(ex24, opening24, p24, carry)
ex24.write(os.path.join(OUT, f"{SIREN}FEC20241231.txt"))

# ====================================================================== 2025 et anomalies
opening25, res24 = opening_from(ex24, sc24, sf24)
ANOM = {}

def apport_cc(ex, oc, of):
    ex.add('BQ', dt.date(2025, 6, 12), 'CCA2025-06', "Apport en compte courant d'associe", [('512000', None, 80000, 0), ('455100', None, 0, 80000)])

def affectation(ex, oc, of):
    if res24 > 0:
        ex.add('OD', dt.date(2025, 6, 30), 'AGO2024', 'Affectation du resultat 2024', [('120000', None, r2(res24), 0), ('110000', None, 0, r2(res24))])

def creance_bloquee(ex, oc, of):
    # A2 : grosse facture Clinique du Parc de février, jamais réglée
    ht = 40000.0
    e = ex.add('VT', dt.date(2025, 2, 14), 'FA2025-0900', 'Facture FA2025-0900 Clinique du Parc amenagement accueil',
               [('411000', 'C006', 48000, 0), ('701000', None, 0, ht), ('445710', None, 0, 8000)])
    e['lines'][0]['never'] = True
    oc.append((e['lines'][0], dt.date(2026, 12, 31)))
    ANOM['A2'] = e

def doublon(ex, oc, of):
    # A5 : facture fournisseur saisie deux fois
    for k in range(2):
        e = ex.add('AC', dt.date(2025, 5, 22), 'F003-2291', 'Facture Vernis et Finitions F003-2291',
                   [('601000', None, 12000, 0), ('445660', None, 2400, 0), ('401000', 'F003', 0, 14400)])
        if k == 0:
            of.append((e['lines'][2], dt.date(2025, 7, 10)))
        else:
            e['lines'][2]['never'] = True; of.append((e['lines'][2], dt.date(2026, 12, 31))); ANOM['A5'] = e

def desequilibre(ex, oc, of):
    # A1 : écriture déséquilibrée de 150 €
    ANOM['A1'] = ex.add('OD', dt.date(2025, 9, 30), 'OD2025-09-REG', 'Regularisation frais de deplacement',
                        [('625100', None, 1250, 0), ('401000', 'F007', 0, 1100)])

def coupure(ex, oc, of):
    # A4 : grosse facture le 30/12, réglée en février 2026 (hors exercice)
    e = ex.add('VT', dt.date(2025, 12, 30), 'FA2025-0901', 'Facture FA2025-0901 Agence Mobilis amenagement siege',
               [('411000', 'C002', 96000, 0), ('701000', None, 0, 80000), ('445710', None, 0, 16000)])
    oc.append((e['lines'][0], dt.date(2026, 2, 15)))
    ANOM['A4'] = e

ca25 = [r2(1400000 / 12 * s) for s in (0.95, 0.95, 1.05, 1.0, 1.05, 1.05, 0.95, 0.7, 1.0, 1.1, 1.1, 1.1)]
ex25 = Exercice(2025)
p25 = dict(ca=ca25, taux_matieres=0.47, salaires=50000, delai_clients=(45, 80), delai_fourn=(55, 75), stock_final=61000,
           urssaf_impayes={9, 10, 11}, hooks=[apport_cc, affectation, creance_bloquee, doublon, desequilibre, coupure])
# TVA de la facture de coupure et de la créance bloquée : intégrée à la déclaration du mois concerné via les hooks ? Non :
# les hooks passent après les déclarations mensuelles, on ajoute donc deux déclarations complémentaires.
sc25, sf25 = run_year(ex25, opening25, p25, carry)
ex25.add('OD', dt.date(2025, 2, 28), 'CA3-202502C', 'Declaration TVA complementaire 02/2025', [('445710', None, 8000, 0), ('445510', None, 0, 8000)])
ex25.add('BQ', dt.date(2025, 3, 20), 'TVA202502C', 'Reglement TVA complementaire 02/2025', [('445510', None, 8000, 0), ('512000', None, 0, 8000)])
ex25.add('OD', dt.date(2025, 5, 31), 'CA3-202505C', 'Declaration TVA complementaire 05/2025', [('445510', None, 4800, 0), ('445660', None, 0, 4800)])
ex25.add('OD', dt.date(2025, 12, 31), 'CA3-202512C', 'Declaration TVA complementaire 12/2025', [('445710', None, 16000, 0), ('445510', None, 0, 16000)])
ex25.write(os.path.join(OUT, f"{SIREN}FEC20251231.txt"))

# ====================================================================== synthèse pour vérification
for ex in (ex24, ex25):
    b = ex.balances()
    td = sum(l['d'] for e in ex.entries for l in e['lines']); tc = sum(l['c'] for e in ex.entries for l in e['lines'])
    ca = -sum(v for k, v in b.items() if k.startswith('70'))
    res = -sum(v for k, v in b.items() if k[0] in '67')
    cp = -sum(b.get(k, 0) for k in ('101300', '106100', '110000', '120000')) + res
    print(ex.year, 'lignes', sum(len(e['lines']) for e in ex.entries), 'ecritures', len(ex.entries),
          'D-C', r2(td - tc), 'CA', r2(ca), 'resultat', r2(res), 'banque', r2(b['512000']), 'URSSAF', r2(b['431000']),
          'clients', r2(b['411000']), 'fourn', r2(b['401000']), 'CP', r2(cp))
