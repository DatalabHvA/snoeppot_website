import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from pynput import keyboard
import io
import dropbox
import xlsxwriter

st.set_page_config(layout="wide")

# Streamlit app
def main():
	
	if "i" not in st.session_state: 
		st.session_state['i'] = 0
     
	if "guesses" not in st.session_state:	
		st.session_state["guesses"] = []
	
	st.title("Raad het aantal snoepjes in de pot")
	st.write("Voer je schatting en e-mailadres in om mee te doen!")
	t = st.empty()
	t.text(f"Aantal deelnemers tot nu toe: {st.session_state['i']}")

	col1, col2 = st.columns(2)

	with col1:
		with st.form(key="guess_form", clear_on_submit=True):
			email = st.text_input("E-mailadres")
			guess = st.number_input("Je schatting van het aantal knikkers", min_value=0, step=1)
			submit = st.form_submit_button("Verstuur")

	if submit:
		if email and guess is not None:
			# Add guess to in-memory storage
			st.session_state['i']+=1
			with col1:
				t.text(f"Aantal deelnemers tot nu toe: {st.session_state['i']}")
				st.session_state["guesses"].append({"E-mailadres": email, "Schatting": int(guess)})
				st.success("Bedankt voor je inzending!")
            
			with col2:
				# Display histogram
				hist1 = st.empty()
				hist2 = st.empty()
	  
				fig, ax = plt.subplots(figsize=(6, 2.2))  # Ensure the histogram fits on screen
				ax.hist(pd.DataFrame(st.session_state["guesses"])['Schatting'], bins=10, color="blue", edgecolor="black")
				ax.set_title("Verdeling van schattingen")
				ax.set_xlabel("Aantal snoepjes")
				ax.set_ylabel("Frequentie")
				hist2.pyplot(fig)

				# Wait for 5 seconds and clear the histogram
				time.sleep(10)
				hist1.empty()
				hist2.empty()
			
		else:
			st.error("Vul alle velden in!")

	with col1:
		st.markdown('#')
		st.markdown('#')
		st.markdown('#')
		st.markdown('#')
		st.markdown('#')
		st.markdown('#')
		st.markdown('#')
		st.markdown('#')
		st.markdown('#')
		st.markdown('#')
		st.markdown('#')
		# Secret download section
		toegang = st.text_input("Enter admin password to download results:", type="password")
		if toegang == "admin1234":
			buffer = io.BytesIO()
			with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
				pd.DataFrame(st.session_state["guesses"]).to_excel(writer, index=False, sheet_name='Guesses')
				writer.close()
				st.download_button(label="Download Results as Excel", data=buffer.getvalue(), file_name="guesses.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
	main()
