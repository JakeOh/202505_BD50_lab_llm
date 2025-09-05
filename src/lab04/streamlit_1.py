import streamlit as st
import pandas as pd
import numpy as np


def main():
    st.title('처음 만들어 본 Streamlit 앱')
    st.write('안녕하세요. 저는 오쌤입니다.')

    df = pd.DataFrame({
        'X1': np.arange(1, 6),
        'X2': np.random.randint(100, size=5)
    })
    # st.write(df)
    st.dataframe(df)


if __name__ == '__main__':
    main()
