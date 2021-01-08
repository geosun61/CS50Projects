# Project 0

Web Programming with Python and JavaScript

## Introduction
My project is a little about my interests, my experiences and skills I learned from my course at Humber College in the Computer Engineering Technology program. The website has 4 pages on 4 different topics first page is the homepage where it is just a summarization about me. The second page is about my capstone project I worked on at Humber College. Third page is about my work experiences and my Technical Skills, it is sorted like a resume. Lastly, the fourth page is just about my general interests and hobbies. All pages have hyperlinks to each page, use SCSS and the Bootstrap stylesheet

## Homepage
This is the page where I give a summary about what is mentioned in the website.
### homepage.html
This html file uses examples of Bootstrap containers, rows and columns. It has examples of an image, lists and 2 brief summaries in paragraph elements one about who I am and the other is about my
capstone project at Humber College.
### homepage.scss
The stylesheet gives examples of a class, id, and *class>element* selector. It also has an import statement used with SCSS to import all the header stylings.

## Capstone Page
This page is about my Capstone project that I worked on at Humber College.
### capstone.html
This html file has an example for the **media** query for styling. I describe the sensors in my project with an image and a brief description of how they were used in my project. The **media** query is used to define if the page reaches a max-width of 800px it will not display the images of class *.senImg* which is all of the sensor images in the table.
### capstone.scss
This stylesheet gives examples for SCSS nesting and once converted to CSS it will result them in the ./cssout/ folder as descendant selectors.

## Experience Page
This page is about my technical skills learned and my work experiences.
### resume.html
This page has examples of bold elements, a media query for printing, and lists. This page also has an example of a Bootstrap component called Card. The card is used for describing my work experience in a header and a body. Header has the company and position I worked and the card body has a list for a description of the position.
### resume.scss
This styling sheet has an import for header and two descendant selectors for the body.

## Hobbies Page
This page is about some of the hobbies I enjoy.
### hobbies.html
This page has images, uses Bootstrap columns and rows, paragraphs and headings.
### hobbies.scss
The styling sheet uses import statement for header, nesting, descendant and a **div > img** selector.

## header.scss
This sass file uses a variable to define a pixel size for padding. An inheritance example is used to define the header.

### cssout folder
The folder holds all CSS converted files from SCSS. 

### img folder
The folder holds all the images.
