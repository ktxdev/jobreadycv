from fontTools.misc.plistlib import end_date
from fpdf import FPDF
from fpdf import XPos, YPos
from app.schema import Resume

MARGIN = 12.7
LINE_HEIGHT = 6
BULLET_POINT = "•"


def validate_and_format_date(date) -> str:
    if not date:
        return ''

    try:
        return date.strftime('%b %Y')
    except ValueError:
        return ''


class ResumePDF(FPDF):
    def __init__(self, font_name):
        super().__init__()
        self.font_name = font_name
        self.set_margin(MARGIN)
        self.add_font(font_name, '', f'app/static/fonts/{font_name}-Regular.ttf')
        self.add_font(font_name, 'B', f'app/static/fonts/{font_name}-Bold.ttf')
        # Get page width taking margins into consideration
        self.page_width = self.w - 2 * self.l_margin

    def add_text(self, w: float, h: float, text, x: XPos = XPos.RIGHT, y:YPos = YPos.TOP, bold: bool = False, font_size: int = 10, align: str = 'L'):
        self.set_font(self.font_name, 'B' if bold else '', font_size)
        self.cell(w, h, text, new_x = x, new_y = y, align = align)

    def add_multiline_text(self, w: float, h: float, text, x: XPos = XPos.RIGHT, y:YPos = YPos.TOP, bold: bool = False, font_size: int = 10, align: str = 'L'):
        self.set_font(self.font_name, 'B' if bold else '', font_size)
        self.multi_cell(w, h, text, new_x = x, new_y = y, align = align)

    def add_horizontal_line(self):
        """
        Draws a horizontal line at the current Y position of the PDF
        """
        # Get current X and Y positions
        x = self.get_x()
        y = self.get_y()

        self.line(x, y, x + self.page_width, y)

    def add_vertical_space(self):
        """
        Inserts a space of 0.5 h at current Y position of the PDF
        """
        self.cell(0, 0.5, '', new_x = XPos.LMARGIN, new_y = YPos.NEXT)

    def add_section_title(self, title: str):
        """
        Adds a title to the PDF with a horizontal line below

        :param title: The title of the section
        """
        self.add_text(0, LINE_HEIGHT, title.upper(), XPos.LMARGIN, YPos.NEXT, True, 10, 'C')
        self.add_horizontal_line()
        self.add_vertical_space()

    def add_bullet(self):
        self.add_text(5, LINE_HEIGHT, BULLET_POINT, XPos.RIGHT, YPos.TOP, True, 14)

    def add_bullet_point(self, point: str):
        self.add_text(5, LINE_HEIGHT, BULLET_POINT, XPos.RIGHT, YPos.TOP, True, 14)
        self.add_multiline_text(0, LINE_HEIGHT, point, XPos.LMARGIN, YPos.NEXT, align = 'J')

    def set_left_and_right_margins(self, margin: float):
        self.set_left_margin(margin)
        self.set_right_margin(margin)

    def generate_resume(self, resume: Resume, output_path: str):
        self.add_page()

        # Add name
        self.add_text(0, LINE_HEIGHT, resume.full_name, XPos.LMARGIN, YPos.NEXT, True, 16, 'C')

        # Add information text
        info_text = (f"{resume.location} {BULLET_POINT} {resume.phone_number} {BULLET_POINT}"
                     f" {resume.email} {BULLET_POINT} {resume.linkedin_url}")
        self.add_text(0, LINE_HEIGHT, info_text, XPos.LMARGIN, YPos.NEXT, font_size = 9, align = 'C')

        # Add education
        self.add_section_title("education")

        for education in resume.education:
            self.add_text(self.page_width / 2, LINE_HEIGHT, f"{education.institution}, {education.location}", font_size = 11)
            timeline = f"{'CURRENT' if education.is_current else validate_and_format_date(education.graduation_date)}"
            self.add_text(self.page_width / 2, LINE_HEIGHT, timeline, font_size = 11, x = XPos.LMARGIN, y = YPos.NEXT, align = 'R')
            self.add_text(0, LINE_HEIGHT, education.program_name, bold = True, font_size = 10, x = XPos.LMARGIN, y = YPos.NEXT)

        # Add professional experience
        self.add_section_title("Professional Experience")

        for experience in resume.experience:
            self.add_text(self.page_width / 2, LINE_HEIGHT, f"{experience.company}, {experience.location}", font_size = 11)

            start_dates = [position.start_date for position in experience.positions if position.start_date]
            start_date = min(start_dates) if start_dates else None
            end_dates = [position.end_date for position in experience.positions if position.end_date]
            end_date = max(end_dates) if end_dates else None
            is_current = any([position.is_current for position in experience.positions])

            timeline = f"{validate_and_format_date(start_date)} – {'Present' if is_current else validate_and_format_date(end_date)}"

            self.add_text(self.page_width / 2, LINE_HEIGHT, timeline, x = XPos.LMARGIN, y = YPos.NEXT, align = 'R')

            for position in experience.positions:
                self.add_text(0, LINE_HEIGHT, f"{position.title}", bold = True, font_size = 10, x = XPos.LMARGIN, y = YPos.NEXT)

                self.set_left_and_right_margins(MARGIN + 2)

                for achievement in position.achievements:
                    self.add_bullet_point(achievement.description)

                self.add_vertical_space()
                self.set_left_and_right_margins(MARGIN)

        # Add Skills
        self.add_section_title("skills")
        self.add_vertical_space()
        for idx, skill in enumerate(resume.skills):
            x = XPos.RIGHT if idx == 0 or idx % 4 != 3 else XPos.LMARGIN
            y = YPos.TOP if idx == 0 or idx % 4 != 3 else YPos.NEXT

            self.add_bullet()
            self.add_text(self.page_width / 4, LINE_HEIGHT, f"{skill.name}", x, y)

        self.output(output_path)

def create_resume_pdf(resume: Resume, output_path: str):
    resume_pdf = ResumePDF("Montserrat")
    resume_pdf.generate_resume(resume, output_path)

