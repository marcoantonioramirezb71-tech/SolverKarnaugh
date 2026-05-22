import streamlit as st
from sympy import symbols, SOPform
from sympy.logic.boolalg import Or, And, Not

# ======================================
# CONFIGURACIÓN
# ======================================

st.set_page_config(
    page_title="Solver MapKarnaugh By MARB",
    layout="wide"
)

st.title("Solver MapKarnaugh By MARB")
st.caption("Fac. Electrónica UPAEP")

# ======================================
# MEMORIA
# ======================================

if "kmap_values" not in st.session_state:
    st.session_state.kmap_values={}

if "vars_order" not in st.session_state:
    st.session_state.vars_order=["A","B","C","D"]

if "output_name" not in st.session_state:
    st.session_state.output_name="F"

# ======================================
# SUPERIOR
# ======================================

c1,c2,c3,c4=st.columns([1,1,2,2])

with c1:

    nvars=st.selectbox(
        "Variables",
        [2,3,4],
        index=2
    )


with c2:

    if st.button("Invertir"):

        st.session_state.vars_order.reverse()

        st.rerun()


with c3:

    st.write("Variables")

    var_cols=st.columns(4)

    for i in range(4):

        st.session_state.vars_order[i]=(
            var_cols[i].text_input(
                "",
                st.session_state.vars_order[i],
                key=f"var{i}"
            )
        )


with c4:

    salida=st.text_input(
        "Salida",
        st.session_state.output_name
    )

    st.session_state.output_name=salida


names=st.session_state.vars_order[:nvars]

# ======================================
# GRAY
# ======================================

if nvars==4:

    rows=4
    cols=4

    row_codes=[
        "00","01",
        "11","10"
    ]

    col_codes=[
        "00","01",
        "11","10"
    ]

elif nvars==3:

    rows=2
    cols=4

    row_codes=[
        "0","1"
    ]

    col_codes=[
        "00","01",
        "11","10"
    ]

else:

    rows=2
    cols=2

    row_codes=[
        "0","1"
    ]

    col_codes=[
        "0","1"
    ]


# ======================================
# INICIALIZAR MAPA
# ======================================

for r in range(rows):

    for c in range(cols):

        if (r,c) not in st.session_state.kmap_values:

            st.session_state.kmap_values[(r,c)]="0"


# ======================================
# VARIABLES ENCABEZADO
# ======================================

if nvars==4:

    fila=names[0]+names[1]
    columna=names[2]+names[3]

elif nvars==3:

    fila=names[0]
    columna=names[1]+names[2]

else:

    fila=names[0]
    columna=names[1]


st.markdown("---")

a,b,c=st.columns([1,4,1])

with b:

    st.markdown(
    f"""
    ### {fila} / {columna}
    """
    )


# ======================================
# ENCABEZADOS COLUMNAS
# ======================================

head=st.columns(cols+1)

head[0].write("")

for c in range(cols):

    head[c+1].markdown(
        f"### {col_codes[c]}"
    )


# ======================================
# MAPA
# ======================================

for r in range(rows):

    line=st.columns(cols+1)

    line[0].markdown(
        f"### {row_codes[r]}"
    )

    for c in range(cols):

        valor=st.session_state.kmap_values[(r,c)]

        if valor=="0":

            icono="⬜"

        elif valor=="1":

            icono="🟩"

        else:

            icono="🟨"

        texto=f"{icono} {valor}"

        if line[c+1].button(
            texto,
            key=f"{r}{c}"
        ):

            if valor=="0":

                st.session_state.kmap_values[
                    (r,c)
                ]="1"

            elif valor=="1":

                st.session_state.kmap_values[
                    (r,c)
                ]="X"

            else:

                st.session_state.kmap_values[
                    (r,c)
                ]="0"

            st.rerun()


# ======================================
# SIMPLIFICACIÓN
# ======================================

minterms=[]
dontcares=[]

for r in range(rows):

    for c in range(cols):

        bits=(
            row_codes[r]
            +
            col_codes[c]
        )

        index=int(
            bits,
            2
        )

        valor=st.session_state.kmap_values[
            (r,c)
        ]

        if valor=="1":

            minterms.append(
                index
            )

        elif valor=="X":

            dontcares.append(
                index
            )


variables=symbols(
    " ".join(names)
)

expr=SOPform(
    variables,
    minterms,
    dontcares
)

# ======================================
# FORMATO
# ======================================

def format_expression(expr):

    if expr==True:
        return "1"

    if expr==False:
        return "0"

    if isinstance(expr,Or):
        terms=expr.args
    else:
        terms=[expr]

    salida=[]

    for term in terms:

        variables={}

        if term.is_Symbol:

            variables[
                str(term)
            ]=False

        elif isinstance(
            term,
            Not
        ):

            variables[
                str(
                    term.args[0]
                )
            ]=True

        elif isinstance(
            term,
            And
        ):

            for f in term.args:

                if isinstance(
                    f,
                    Not
                ):

                    variables[
                        str(
                            f.args[0]
                        )
                    ]=True

                else:

                    variables[
                        str(f)
                    ]=False

        txt=""

        for v in names:

            if v in variables:

                if variables[v]:

                    txt+=v+"'"

                else:

                    txt+=v

        salida.append(txt)

    return " + ".join(salida)


texto=format_expression(expr)

st.markdown("---")

st.markdown(
f"# {st.session_state.output_name} = {texto}"
)