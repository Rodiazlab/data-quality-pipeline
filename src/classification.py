import pandas as pd

from src.validation import (
    find_duplicates,
    find_missing_values,
    find_invalid_emails,
)

# clasifica los registros en un DataFrame según la calidad de los datos y devuelve una serie con las etiquetas de calidad de datos
def classify_records(  
        
    dataframe: pd.DataFrame, 
    parsed_dates: pd.Series,
    parsed_amounts: pd.Series,
) -> pd.Series: 
   
    quality_issues = pd.Series( 
        "",
        index=dataframe.index,
        dtype="string",
    )   

    missing_customer_id = find_missing_values( #  busca registros con valores faltantes en la columna "customer_id" y devuelve una serie de booleanos indicando si hay valores faltantes o no.
        dataframe,
        "customer_id",
    )
    quality_issues.loc[missing_customer_id] = ( # después, para los registros con valores faltantes en "customer_id", se agrega la etiqueta "MISSING_CUSTOMER_ID" a la serie de calidad de datos.
        quality_issues.loc[missing_customer_id]
        + "MISSING_CUSTOMER_ID|"
    )

    missing_email = find_missing_values( #    busca registros con valores faltantes en la columna "email" y devuelve una serie de booleanos indicando si hay valores faltantes o no.
        dataframe,
        "email",
    )
    quality_issues.loc[missing_email] = ( # después, para los registros con valores faltantes en "email", se agrega la etiqueta "MISSING_EMAIL" a la serie de calidad de datos.
        quality_issues.loc[missing_email]
        + "MISSING_EMAIL|"
    )
    duplicate_customer_id = find_duplicates( # busca registros duplicados en la columna "customer_id" y devuelve un booleano indicando si hay duplicados o no.
        dataframe, 
        "customer_id",
    )
    quality_issues.loc[duplicate_customer_id] = ( # después, para los registros duplicados en "customer_id", se agrega la etiqueta "DUPLICATED_CUSTOMER_ID" a la serie de calidad de datos.
        quality_issues.loc[duplicate_customer_id]
        + "DUPLICATED_CUSTOMER_ID|"
    )

    invalid_email = find_invalid_emails( # busca registros con correos electrónicos inválidos y devuelve una serie de booleanos indicando si el mail es invalido".
        dataframe,
        "email",
    )
    quality_issues.loc[invalid_email] = ( # después, para los registros con correos electrónicos inválidos, se agrega la etiqueta "INVALID_EMAIL" a la serie de calidad de datos.
        quality_issues.loc[invalid_email]
        + "INVALID_EMAIL|"
    )

    invalid_signup_date = parsed_dates.isna() # busca registros con fechas de registro inválidas y devuelve una serie de booleanos indicando si la fecha es inválida o no.
    quality_issues.loc[invalid_signup_date] = ( # después, para los registros con fechas de registro inválidas, se agrega la etiqueta "INVALID_SIGNUP_DATE" a la serie de calidad de datos.
        quality_issues.loc[invalid_signup_date]
        + "INVALID_SIGNUP_DATE|"
    )

    invalid_amount = parsed_amounts.isna() # busca registros con montos inválidos y devuelve una serie de booleanos indicando si el monto es inválido o no.
    quality_issues.loc[invalid_amount] = ( # después, para los registros con montos inválidos, se agrega la etiqueta "INVALID_AMOUNT" a la serie de calidad de datos.               
        quality_issues.loc[invalid_amount]
        + "INVALID_AMOUNT|"
    )   
    negative_amount = parsed_amounts < 0 # busca registros con montos negativos y devuelve una serie de booleanos indicando si el monto es negativo o no.
    quality_issues.loc[negative_amount] = ( # después, para los registros con montos negativos, se agrega la etiqueta "NEGATIVE_AMOUNT" a la serie de calidad de datos.             
        quality_issues.loc[negative_amount]
        + "NEGATIVE_AMOUNT|"
    )       


    return quality_issues.str.rstrip("|")

