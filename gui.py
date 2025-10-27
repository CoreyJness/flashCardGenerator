from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
import asyncio
import threading
from datetime import datetime
from main import gatherMaterials, chooseFormat, qWriting


class FlashCardLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # Title
        title = Label(
            text="Flashcard Generator",
            size_hint_y=None,
            height=50,
            font_size='24sp',
            bold=True
        )
        self.add_widget(title)

        # Input section
        input_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=100)
        
        input_grid.add_widget(Label(text="Topic:", size_hint_x=0.3))
        self.topic_input = TextInput(
            multiline=False,
            hint_text="e.g., World War II"
        )
        input_grid.add_widget(self.topic_input)

        input_grid.add_widget(Label(text="Format:", size_hint_x=0.3))
        self.format_spinner = Spinner(
            text='Quizlet',
            values=('Quizlet', 'Kahoot', 'Gimkit'),
            size_hint_x=0.7
        )
        input_grid.add_widget(self.format_spinner)
        
        self.add_widget(input_grid)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.generate_button = Button(
            text="Generate Flashcards",
            background_color=(0.2, 0.6, 1, 1)
        )
        self.generate_button.bind(on_press=self.on_generate)
        button_layout.add_widget(self.generate_button)

        self.save_button = Button(
            text="Save to File",
            background_color=(0.2, 0.8, 0.2, 1),
            disabled=True
        )
        self.save_button.bind(on_press=self.on_save)
        button_layout.add_widget(self.save_button)

        self.add_widget(button_layout)

        # Status label
        self.status_label = Label(
            text="Ready to generate flashcards",
            size_hint_y=None,
            height=30,
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(self.status_label)

        # Output section with scrollview
        output_label = Label(
            text="Generated Flashcards:",
            size_hint_y=None,
            height=30,
            bold=True
        )
        self.add_widget(output_label)

        scroll = ScrollView(size_hint=(1, 1))
        self.output_text = TextInput(
            text="",
            multiline=True,
            readonly=True,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1)
        )
        scroll.add_widget(self.output_text)
        self.add_widget(scroll)

        # Store generated content
        self.generated_content = ""

    def on_generate(self, instance):
        subject = self.topic_input.text.strip()
        
        if not subject:
            self.update_status("⚠️ Please enter a topic", error=True)
            return

        # Disable button during generation
        self.generate_button.disabled = True
        self.save_button.disabled = True
        self.update_status("🔄 Gathering materials from Encyclopedia.com...")
        self.output_text.text = "Processing... This may take 30-60 seconds.\n\n"

        # Get format choice
        format_map = {'Quizlet': '1', 'Kahoot': '2', 'Gimkit': '3'}
        format_choice = format_map.get(self.format_spinner.text, '1')

        # Run in separate thread to avoid blocking UI
        thread = threading.Thread(
            target=self.run_generation_thread,
            args=(subject, format_choice)
        )
        thread.daemon = True
        thread.start()

    def run_generation_thread(self, subject, format_choice):
        """Run async operations in a separate thread with its own event loop"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the async generation
            loop.run_until_complete(self.generate_flashcards(subject, format_choice))
            
        except Exception as e:
            self.handle_error(str(e))
        finally:
            loop.close()

    async def generate_flashcards(self, subject, format_choice):
        """Async function to generate flashcards"""
        try:
            # Gather materials
            self.update_status("📚 Scraping encyclopedia content...")
            page_data = await gatherMaterials(subject)
            
            # Generate questions
            self.update_status("🤖 Generating flashcards with AI...")
            selected_format = chooseFormat(format_choice)
            self.generated_content = qWriting(page_data, selected_format)
            
            # Update UI on main thread
            self.display_results(subject, selected_format['name'])
            
        except Exception as e:
            self.handle_error(str(e))

    @mainthread
    def update_status(self, message, error=False):
        """Update status label (called from any thread)"""
        self.status_label.text = message
        if error:
            self.status_label.color = (1, 0.3, 0.3, 1)
        else:
            self.status_label.color = (0.7, 0.7, 0.7, 1)

    @mainthread
    def display_results(self, subject, format_name):
        """Display generated flashcards (called from worker thread)"""
        self.output_text.text = self.generated_content
        self.update_status(f"✅ Generated {len(self.generated_content.splitlines())} items for '{subject}' ({format_name})")
        self.generate_button.disabled = False
        self.save_button.disabled = False

    @mainthread
    def handle_error(self, error_msg):
        """Handle errors (called from worker thread)"""
        self.output_text.text = f"❌ Error occurred:\n\n{error_msg}\n\nPlease try again or choose a different topic."
        self.update_status("❌ Generation failed", error=True)
        self.generate_button.disabled = False

    def on_save(self, instance):
        """Save generated content to file"""
        if not self.generated_content:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        format_name = self.format_spinner.text.lower()
        subject = self.topic_input.text.strip().replace(' ', '_')
        
        filename = f"{subject}_{format_name}_{timestamp}.csv"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.generated_content)
            self.update_status(f"💾 Saved to {filename}")
        except Exception as e:
            self.update_status(f"❌ Save failed: {str(e)}", error=True)


class FlashCardGenerator(App):
    def build(self):
        Window.size = (800, 600)
        return FlashCardLayout()


if __name__ == '__main__':
    FlashCardGenerator().run()