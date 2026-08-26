# -*- coding: utf-8 -*-
"""
Calculadora de Financiamento — versão Python (Kivy)
Mesmo modelo visual e mesma lógica de cálculo do preview HTML:
- Entrada = % sobre o valor do produto (paga à parte, não entra no parcelamento)
- TAC automática: > R$ 1000 -> R$ 120 | <= R$ 1000 -> R$ 80
- Parcelas calculadas com juros compostos (Tabela Price) de 2,99% ao mês
  sobre o valor financiado (o valor_principal, sem a entrada)
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Taxa de juros fixa do financiamento: 2,99% ao mês
TAXA_JUROS_MENSAL = 0.0299


def fmt_moeda(valor):
    """Formata um número no padrão R$ 1.234,56"""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def calcular_parcela_com_juros(valor_financiado, taxa_mensal, num_parcelas):
    """Tabela Price — mesma lógica usada no preview HTML (calcularParcelaComJuros)."""
    if taxa_mensal == 0:
        return valor_financiado / num_parcelas
    i = taxa_mensal
    fator = 1 - (1 + i) ** (-num_parcelas)
    return (valor_financiado * i) / fator


KV = """
#:import Window kivy.core.window.Window

<GradientHeader@BoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: dp(190)
    padding: dp(20), dp(22), dp(20), dp(30)
    spacing: dp(4)
    canvas.before:
        Color:
            rgba: 0.043, 0.165, 0.357, 1   # blue-900
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.122, 0.373, 0.839, 0.55  # blue-600 overlay (aprox. gradiente)
        Rectangle:
            pos: self.x, self.y
            size: self.width, self.height * 0.6

    Label:
        text: "SIMULADOR DE CRÉDITO"
        color: 1, 1, 1, 0.75
        font_size: "11sp"
        bold: True
        halign: "left"
        valign: "top"
        size_hint_y: None
        height: dp(16)
        text_size: self.size

    Label:
        text: "Calculadora de\\nFinanciamento"
        color: 1, 1, 1, 1
        font_size: "24sp"
        bold: True
        halign: "left"
        valign: "top"
        size_hint_y: None
        height: dp(66)
        text_size: self.size

    Label:
        text: "Entrada, TAC e juros calculados automaticamente"
        color: 1, 1, 1, 0.85
        font_size: "13sp"
        halign: "left"
        valign: "top"
        size_hint_y: None
        height: dp(18)
        text_size: self.size


<RoundedCard@BoxLayout>:
    orientation: "vertical"
    padding: dp(18)
    spacing: dp(14)
    size_hint_y: None
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(18)]

<FieldLabel@Label>:
    color: 0.42, 0.47, 0.58, 1
    font_size: "12.5sp"
    bold: True
    halign: "left"
    valign: "middle"
    size_hint_y: None
    height: dp(18)
    text_size: self.size

<InputBox@BoxLayout>:
    size_hint_y: None
    height: dp(46)
    canvas.before:
        Color:
            rgba: 0.91, 0.94, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]
        Color:
            rgba: 0.87, 0.90, 0.96, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, dp(12))
            width: 1.2

<ResultLine@BoxLayout>:
    size_hint_y: None
    height: dp(34)
    canvas.before:
        Color:
            rgba: 0.875, 0.90, 0.96, 1
        Line:
            points: [self.x, self.y, self.right, self.y]
            width: 1

<PrimaryButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0.122, 0.373, 0.839, 1
    color: 1, 1, 1, 1
    bold: True
    font_size: "15sp"
    size_hint_y: None
    height: dp(50)
    canvas.before:
        Color:
            rgba: 0.122, 0.373, 0.839, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]

<StepperButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    bold: True
    font_size: "20sp"
    size_hint_x: None
    width: dp(46)
    canvas.before:
        Color:
            rgba: 0.122, 0.373, 0.839, 1
        Rectangle:
            pos: self.pos
            size: self.size


ScreenManager:
    MainScreen:

<MainScreen>:
    name: "main"
    canvas.before:
        Color:
            rgba: 0.91, 0.94, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    ScrollView:
        do_scroll_x: False
        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            spacing: 0

            GradientHeader:

            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16), dp(0), dp(16), dp(30)
                spacing: dp(16)
                pos_hint: {"top": 1}

                Widget:
                    size_hint_y: None
                    height: dp(10)

                RoundedCard:
                    id: card_form
                    height: self.minimum_height

                    FieldLabel:
                        text: "Valor do produto"

                    InputBox:
                        Label:
                            text: "R$"
                            bold: True
                            color: 0.07, 0.29, 0.65, 1
                            size_hint_x: None
                            width: dp(28)
                            padding: dp(12), 0
                        TextInput:
                            id: valor_input
                            hint_text: "0,00"
                            input_filter: "float"
                            multiline: False
                            background_normal: ""
                            background_active: ""
                            background_color: 0, 0, 0, 0
                            foreground_color: 0.06, 0.11, 0.2, 1
                            font_size: "16sp"
                            padding: [0, dp(12), dp(12), 0]

                    FieldLabel:
                        text: "Porcentagem de entrada"

                    InputBox:
                        TextInput:
                            id: porcentagem_input
                            hint_text: "0"
                            input_filter: "float"
                            multiline: False
                            background_normal: ""
                            background_active: ""
                            background_color: 0, 0, 0, 0
                            foreground_color: 0.06, 0.11, 0.2, 1
                            font_size: "16sp"
                            padding: [dp(12), dp(12), 0, 0]
                        Label:
                            text: "%"
                            bold: True
                            color: 0.07, 0.29, 0.65, 1
                            size_hint_x: None
                            width: dp(28)

                    FieldLabel:
                        text: "Calculada sobre o valor do produto e paga a parte"
                        font_size: "11sp"
                        bold: False
                        height: dp(14)

                    FieldLabel:
                        text: "Quantidade de parcelas"

                    BoxLayout:
                        size_hint_y: None
                        height: dp(46)
                        canvas.before:
                            Color:
                                rgba: 1, 1, 1, 1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(12)]
                            Color:
                                rgba: 0.87, 0.90, 0.96, 1
                            Line:
                                rounded_rectangle: (self.x, self.y, self.width, self.height, dp(12))
                                width: 1.2

                        StepperButton:
                            text: "-"
                            on_release: app.dec_parcelas()

                        Label:
                            id: parcelas_val
                            text: str(app.parcelas) + "x"
                            bold: True
                            color: 0.06, 0.11, 0.2, 1
                            font_size: "16sp"

                        StepperButton:
                            text: "+"
                            on_release: app.inc_parcelas()

                    FieldLabel:
                        text: "Juros de 2,99% ao mes aplicados sobre o valor financiado"
                        font_size: "11sp"
                        bold: False
                        height: dp(14)

                    PrimaryButton:
                        text: "Simular financiamento"
                        on_release: app.calcular()

                RoundedCard:
                    id: card_result
                    height: self.minimum_height if app.mostrar_resultado else 0
                    opacity: 1 if app.mostrar_resultado else 0
                    disabled: not app.mostrar_resultado

                    Label:
                        text: "RESUMO DA SIMULAÇÃO"
                        color: 0.07, 0.29, 0.65, 1
                        bold: True
                        font_size: "11sp"
                        size_hint_y: None
                        height: dp(20) if app.mostrar_resultado else 0
                        halign: "left"
                        valign: "middle"
                        text_size: self.size

                    ResultLine:
                        Label:
                            text: "Valor do produto"
                            color: 0.42, 0.47, 0.58, 1
                            font_size: "13.5sp"
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                        Label:
                            text: app.r_valor
                            bold: True
                            color: 0.06, 0.11, 0.2, 1
                            font_size: "13.5sp"
                            halign: "right"
                            valign: "middle"
                            text_size: self.size

                    ResultLine:
                        Label:
                            text: "Entrada"
                            color: 0.42, 0.47, 0.58, 1
                            font_size: "13.5sp"
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                        Label:
                            text: app.r_entrada
                            bold: True
                            color: 0.06, 0.11, 0.2, 1
                            font_size: "13.5sp"
                            halign: "right"
                            valign: "middle"
                            text_size: self.size

                    ResultLine:
                        Label:
                            text: "TAC (taxa de abertura)"
                            color: 0.42, 0.47, 0.58, 1
                            font_size: "13.5sp"
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                        Label:
                            text: app.r_tac
                            bold: True
                            color: 0.06, 0.11, 0.2, 1
                            font_size: "13.5sp"
                            halign: "right"
                            valign: "middle"
                            text_size: self.size

                    ResultLine:
                        Label:
                            text: "Valor financiado"
                            color: 0.42, 0.47, 0.58, 1
                            font_size: "13.5sp"
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                        Label:
                            text: app.r_financiado
                            bold: True
                            color: 0.06, 0.11, 0.2, 1
                            font_size: "13.5sp"
                            halign: "right"
                            valign: "middle"
                            text_size: self.size

                    BoxLayout:
                        size_hint_y: None
                        height: dp(34)
                        Label:
                            text: "Juros (2,99% a.m.)"
                            color: 0.42, 0.47, 0.58, 1
                            font_size: "13.5sp"
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                        Label:
                            text: app.r_juros
                            bold: True
                            color: 0.753, 0.224, 0.169, 1
                            font_size: "13.5sp"
                            halign: "right"
                            valign: "middle"
                            text_size: self.size

                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(76) if app.mostrar_resultado else 0
                        padding: dp(4), dp(12)
                        canvas.before:
                            Color:
                                rgba: 0.043, 0.165, 0.357, 1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(14)]

                        Label:
                            text: app.r_parcela
                            color: 1, 1, 1, 1
                            bold: True
                            font_size: "22sp"

                        Label:
                            text: "VALOR DE CADA PARCELA"
                            color: 1, 1, 1, 0.85
                            font_size: "10.5sp"

                    BoxLayout:
                        size_hint_y: None
                        height: dp(40) if app.mostrar_resultado else 0
                        Label:
                            text: "Total pago"
                            bold: True
                            color: 0.06, 0.11, 0.2, 1
                            font_size: "16sp"
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                        Label:
                            text: app.r_total
                            bold: True
                            color: 0.06, 0.11, 0.2, 1
                            font_size: "16sp"
                            halign: "right"
                            valign: "middle"
                            text_size: self.size

                    Label:
                        text: "Entrada + TAC + soma de todas as parcelas com juros"
                        color: 0.42, 0.47, 0.58, 1
                        font_size: "11sp"
                        size_hint_y: None
                        height: dp(28) if app.mostrar_resultado else 0
"""


class MainScreen(Screen):
    pass


class CalculadoraApp(App):
    parcelas = NumericProperty(12)
    mostrar_resultado = BooleanProperty(False)

    r_valor = StringProperty("")
    r_entrada = StringProperty("")
    r_tac = StringProperty("")
    r_financiado = StringProperty("")
    r_juros = StringProperty("")
    r_parcela = StringProperty("")
    r_total = StringProperty("")

    def build(self):
        self.title = "Calculadora de Financiamento"
        return Builder.load_string(KV)

    def inc_parcelas(self):
        if self.parcelas < 60:
            self.parcelas += 1

    def dec_parcelas(self):
        if self.parcelas > 1:
            self.parcelas -= 1

    def _erro(self, mensagem):
        popup = Popup(
            title="Verifique os dados",
            content=Label(text=mensagem),
            size_hint=(0.8, 0.3),
        )
        popup.open()

    def calcular(self):
        root = self.root.get_screen("main")
        valor_input = root.ids.valor_input
        porcentagem_input = root.ids.porcentagem_input

        try:
            valor_principal = float((valor_input.text or "").replace(",", "."))
        except ValueError:
            valor_principal = -1
        try:
            porcentagem = float((porcentagem_input.text or "").replace(",", "."))
        except ValueError:
            porcentagem = -1

        if valor_principal <= 0:
            self._erro("Digite um valor do produto valido.")
            return
        if porcentagem < 0:
            self._erro("Digite uma porcentagem de entrada valida.")
            return

        # Entrada = porcentagem sobre o valor do produto (não entra no parcelamento)
        entrada = valor_principal * (porcentagem / 100)

        # TAC automática: acima de R$ 1000 -> R$ 120 | até R$ 1000 -> R$ 80
        tac = 120 if valor_principal > 1000 else 80

        # Valor financiado (parcelado) é só o principal, sem a entrada
        valor_financiado = valor_principal

        # Parcela com juros compostos de 2,99% ao mês (Tabela Price)
        valor_parcela = calcular_parcela_com_juros(
            valor_financiado, TAXA_JUROS_MENSAL, self.parcelas
        )

        total_parcelas = valor_parcela * self.parcelas
        total_juros = total_parcelas - valor_financiado
        total_pago = entrada + tac + total_parcelas

        self.r_valor = fmt_moeda(valor_principal)
        self.r_entrada = f"{fmt_moeda(entrada)} ({porcentagem:.0f}%)"
        self.r_tac = fmt_moeda(tac)
        self.r_financiado = fmt_moeda(valor_financiado)
        self.r_juros = fmt_moeda(total_juros)
        self.r_parcela = f"{self.parcelas}x de {fmt_moeda(valor_parcela)}"
        self.r_total = fmt_moeda(total_pago)

        self.mostrar_resultado = True


if __name__ == "__main__":
    CalculadoraApp().run()
