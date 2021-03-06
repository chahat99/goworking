# vim:fileencoding=utf-8
#  Go Working - Controle das Mesas
#  
#  Copyright (C) 2019-2020 Fábrica do Futuro
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
## Mesas, cadeiras, empresas e habitantes do GoWorking

from datetime import datetime
from sqlalchemy.orm import relationship

from app import db
from blueprints.goworking.controllers import custom_uuid

class espaco_v1(db.Model):
  id = db.Column(db.String(36), primary_key=True, unique=True,
    nullable=False, default=custom_uuid.random_uuid)
  timestamp = db.Column(db.TIMESTAMP, index=True,
    default=datetime.utcnow)

  numero = db.Column(db.String(2), default='00')
  ordem = db.Column(db.Integer(), default=0)
  desc = db.Column(db.Text(), nullable=True)

  mesa = relationship(
    'mesa_v1',
    uselist=False,
    back_populates='espaco',
  )

  def get_id(self):
    return self.id
  def __repr__(self):
    return """<espaco_v1(
  'id: %s',
  'timestamp: %s',
  'numero: %s',
  'ordem: %s',
  'desc: %s',
    )>""" % (
      self.id,
      str(self.timestamp),
      self.numero,
      self.ordem,
      self.desc,
    )

class espaco(espaco_v1):
  pass

class mesa_v1(db.Model):
  id = db.Column(db.String(36), primary_key=True, unique=True,
    nullable=False, default=custom_uuid.random_uuid)
  timestamp = db.Column(db.TIMESTAMP, index=True,
    default=datetime.utcnow)

  numero = db.Column(db.String(2), default='00')
  ordem = db.Column(db.Integer(), default=0)
  desc = db.Column(db.Text(), nullable=True)

  id_espaco = db.Column(db.String(36), db.ForeignKey(espaco_v1.id))

  espaco = relationship(
    'espaco_v1',
    uselist=False,
    back_populates='mesa',
  )
  cadeiras = relationship('cadeira_v1', order_by='cadeira_v1.ordem')

  def get_id(self):
    return self.id
  def __repr__(self):
    return """<mesa_v1(
  'id: %s',
  'timestamp: %s',
  'numero: %s',
  'ordem: %s',
  'desc: %s',
  'id_espaco: %s',
    )>""" % (
      self.id,
      str(self.timestamp),
      self.numero,
      self.ordem,
      self.desc,
      self.id_espaco,
    )

class mesa(mesa_v1):
  pass

class cadeira_v1(db.Model):
  id = db.Column(db.String(36), primary_key=True, unique=True,
    nullable=False, default=custom_uuid.random_uuid)
  timestamp = db.Column(db.TIMESTAMP, index=True,
    default=datetime.utcnow)

  numero = db.Column(db.String(4), default='00-E')
  ordem = db.Column(db.Integer(), default=0)
  desc = db.Column(db.Text(), nullable=True)

  id_mesa = db.Column(db.String(36), db.ForeignKey(mesa_v1.id))

  mesa = relationship('mesa_v1', uselist=False)
  habitante = relationship('habitante_v1', uselist=False)

  def get_id(self):
    return self.id
  def __repr__(self):
    return """<cadeira_v1(
  'id: %s',
  'timestamp: %s',
  'numero: %s',
  'ordem: %s',
  'desc: %s',
  'id_mesa: %s',
    )>""" % (
      self.id,
      str(self.timestamp),
      self.numero,
      self.ordem,
      self.desc,
      self.id_mesa,
    )

class cadeira(cadeira_v1):
  pass

class empresa_v1(db.Model):
  id = db.Column(db.String(36), primary_key=True, unique=True,
    nullable=False, default=custom_uuid.random_uuid)
  timestamp = db.Column(db.TIMESTAMP, index=True,
    default=datetime.utcnow)

  nome = db.Column(db.String(255), index=False, unique=False,
    nullable=False, default=u"Nenhuma")
  cnpj = db.Column(db.String(14), index=False, unique=False,
    nullable=True, default='00000000000000')
  desc = db.Column(db.Text(), nullable=True)

  habitantes = relationship('habitante_v1', order_by='habitante_v1.nome')

  def get_id(self):
    return self.id
  def __repr__(self):
    return """<empresa_v1(
      'id: %s',
      'timestamp: %s',
      'nome: %s',
      'cnpj: %s',
      'desc: %s',
    )>""" % (
      self.id,
      str(self.timestamp),
      self.nome,
      self.cnpj,
      self.desc,
    )

class empresa(empresa_v1):
  pass

class habitante_v1(db.Model):
  id = db.Column(db.String(36), primary_key=True, unique=True,
    nullable=False, default=custom_uuid.random_uuid)
  timestamp = db.Column(db.TIMESTAMP, index=True,
    default=datetime.utcnow)

  nome = db.Column(db.String(255), index=False, unique=False,
    nullable=False, default=u"Ninguém")
  cpf = db.Column(db.String(11), index=False, unique=False,
    nullable=True, default='00000000000')
  desc = db.Column(db.Text(), nullable=True)
  data_entrada = db.Column(db.DateTime, index=False, unique=False,
    nullable=True, default=datetime.utcnow)
  data_saida = db.Column(db.DateTime, index=False, unique=False,
    nullable=True, default=datetime.max)
  data_renovacao = db.Column(db.DateTime, index=False, unique=False,
    nullable=True, default=datetime.utcnow)

  id_cadeira = db.Column(db.String(36), db.ForeignKey(cadeira_v1.id))
  id_empresa = db.Column(db.String(36), db.ForeignKey(empresa_v1.id))

  cadeira = relationship('cadeira_v1', uselist=False)
  empresa = relationship('empresa_v1', uselist=False)

  def get_id(self):
    return self.id
  def __repr__(self):
    return """<habitante_v1(
  'id: %s',
  'timestamp: %s',
  'nome: %s',
  'cpf: %s',
  'desc: %s',
  'data_entrada: %s',
  'data_saida: %s',
  'data_renovacao: %s',
  'id_cadeira: %s',
  'id_empresa: %s',
    )>""" % (
      self.id,
      str(self.timestamp),
      self.nome,
      self.cpf,
      self.desc,
      str(self.data_entrada),
      str(self.data_saida),
      str(self.data_renovacao),
      self.id_cadeira,
      self.id_empresa,
    )

class habitante(habitante_v1):
  pass

#Você sabe como é calculado os dois ultimos algarismos do CNPJ ?
# xx.xxx.xxx/0001-??
#ROTINA PARA CALCULO DO DÍGITO VERIFICADOR DO CNPJ
#O CNPJ é composto de 14 caracteres sendo que os oito primeiros formam o
# número de inscrição(raiz- nº base), os quatro números após a barra 
#representam a quantidades de estabelecimentos inscritos(filiais), e os 
#dois últimos algarismos são os dígitos de verificação.
#Exemplo: CNPJ: 42.318.949/0001-84
#Onde: 42.318.949 = nº base
#/0001 = primeiro estabelecimento inscrito – matriz
#84 = dígitos de verificação
#COMO CALCULAR OS DÍGITOS:
#1º DIGITO:
#Colocar 0 à esquerda do nº + nº do estabelecimento;
#0423189490001
#Multiplicar cada nº acima pelos nºs: 6543298765432 de um em um;
#Cada produto da multiplicação deve ser somado;
#A soma dos produtos, dividir por 11;
#O resto da divisão, subtrair de 11, o resultado será o 1º dígito.
#2º DÍGITO:
#Fazer a mesma operação acima , agora desconsiderando o 0 à esquerda, 
#porém, colocando o 1º digíto, já encontrado, à direito.
#Exemplo prático para o 1º dígito:
#0 4 2 3 1 8 9 4 9 0 0 0 1
#x x x x x x x x x x x x x
#6 5 4 3 2 9 8 7 6 5 4 3 2
#= = = = = = = = = = = = =
#0+ 20+ 8 + 9 + 2 +72+ 72+ 28+ 54 + 0 + 0 + 0 + 2 = 267 / 11 =
#047 24
#03 = resto
#Dígito verificador = 11 – 3 = 8
#Exemplo para 0 2º dígito:
#4 2 3 1 8 9 4 9 0 0 0 1 8
#x x x x x x x x x x x x x
#6 5 4 3 2 9 8 7 6 5 4 3 2
#24=10+12+3+16+81+32+63+ 0+ 0 + 0 + 3 + 16 =
#= 260 / 11
#040 23
#07 = resto
#2º dígito verificador = 11 – 7 = 4
#OBS: quando o resto da divisão for menor ou igual a 1 o dígito será
# igual a 0 
#function ValidarCNPJ(cnpj: int[14]) -> bool
#    var v: int[2]
#    //Nota: Calcula o primeiro dígito de verificação.
#    v[1] := 5×cnpj[1] + 4×cnpj[2]  + 3×cnpj[3]  + 2×cnpj[4]
#    v[1] += 9×cnpj[5] + 8×cnpj[6]  + 7×cnpj[7]  + 6×cnpj[8]
#    v[1] += 5×cnpj[9] + 4×cnpj[10] + 3×cnpj[11] + 2×cnpj[12]
#    v[1] := 11 - v[1] mod 11
#    v[1] := 0 if v[1] ≥ 10
#    //Nota: Calcula o segundo dígito de verificação.
#    v[2] := 6×cnpj[1] + 5×cnpj[2]  + 4×cnpj[3]  + 3×cnpj[4]
#    v[2] += 2×cnpj[5] + 9×cnpj[6]  + 8×cnpj[7]  + 7×cnpj[8]
#    v[2] += 6×cnpj[9] + 5×cnpj[10] + 4×cnpj[11] + 3×cnpj[12]
#    v[2] += 2×cnpj[13]
#    v[2] := 11 - v[2] mod 11
#    v[2] := 0 if v[2] ≥ 10
#    //Nota: Verdadeiro se os dígitos de verificação são os esperados.
#    return v[1] = cnpj[13] and v[2] = cnpj[14]
