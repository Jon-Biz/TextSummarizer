# Transcribing summarizer

This locally hosted web application converts an audio file into a text transcript, then passes it to an LLM along with a system prompt for summarization. The transcript and summary and related  are saved as text and markdown documents respectively. Previous summaries are viewable by the user, and appear in the UI in a sidebar. Settings are stored in a text file alongside the transcripts and markdown summary documents.

# Technology

## Backend
Since the libraries we will access are python based, we will use a python backend with FastAPI endpoints. 

### Audio-to-text
We will use the Faster-Whisper library to perfrom the audio-to-text conversion.

* https://github.com/SYSTRAN/faster-whisper

### Summarization LLM
We will pass chat completion requests to an openai compatible endpoint, stored in the user's setting text file.

## Front end
The front end will be written in Typescript, using the Vite React framework with the Shadcn component library. 

### UI

The UI will be built using React and the Shadcn Component library. It will be comprised of an InteractionPane along with a sidebar. 

The top of the sidebar contains the CurrentItemPane, that contains links to the currently edited content, if any: a link to the current transcript, a link to the current version of the summary.

Below the CurrentItemPane is a list of previous items: the PreviousItems component.

A modal appears when the system is working, letting the user know when the system is warking and what progress being made.

In the top right hand corner is a Settings icon, that opens a larger model containing an editable text area containing the system prompt, and editable fields for the open router model endpoint and open router API key. Editing the text area or fields imediately sets the relative item. The system prompt, end point and api key are saved in a text file alongside the transcripts and summarys

### Behaviors

When the application server is launched:

* it looks for the settings file in the settings directory, copying and saving the default one if there is none there
* it looks for text and markdown files in the data directory, loads any it finds.

When the user visits the web page:

* the page is served.
* the page loads the data from the data endpoint and populates the PreviousItems list with an entry for each pair of text and markdown files

When the user drops an audio file on to the interface:

* the current item in in the InteractionPane and current pane are removed, if present
* the modal is launched to inform the user that that the system is processing their file
* the audio file is passed to the back end, processed into a text transcript and saved to disk. 
* the transcript is passed to the LLM along with the system prompt. If the user has not set a system prompt yet, a default system prompt is used.
* the response of the LLM is then passed to back to the LLM with a system prompt that requests a title for the item.
* the transcript and summary are saved to the data directory with their filename the title for the item.
* the item is added to the list of items in the PreviousItems list
* the item is displayed in the CurrentItemPane and item summary is displayed in the InteractionPane

When a user clicks on an item in the PreviousItems pane:

* the item is displayed in the CurrentItemPane and InteractionPane.
* the InteractionPane displays the summary document

When a user clicks on a link to the transcription or summary in the CurrentItemPane:

* the transcription or summary is displayed in the InteractionPane.