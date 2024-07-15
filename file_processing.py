## IMPORTS
import json
import random
import os

class storyProcessing():
    """ 
        Class to process the story file, from selecting a random story to display to
        determining how to display the data in question.
    """

    def __init__(self) -> None:
        file = open('stories/data_3.json')
        self.__story = json.load(file)
        self.__read_story()
        self.__display_options()
    
    def __read_story(self, scene: str='3', scene_section: str='intro') -> None:
        """ Read story introduction """
        scene = self.__story[scene]
        if isinstance(scene[scene_section], str) == True:
            # Execute if intro is a String
            print(scene[scene_section])

        elif isinstance(scene[scene_section], dict) == True:
            # Execute if intro is a Dictionary
            for paragraph in scene[scene_section]:
                print(scene[scene_section][paragraph])
        
        elif isinstance(scene[scene_section], list) == True:
            # Execute if intro is a List
            # Loop through intro and print the paragraphs
            for paragraph in scene[scene_section]:
                print(paragraph)

    def __display_options(self, scene: str='3', scene_section: str='options') -> None:
        scene = self.__story[scene]
        if isinstance(scene[scene_section], str) == True:
            # Execute if intro is a String
            # This means no options just text
            print(scene[scene_section])

        elif isinstance(scene[scene_section], dict) == True:
            # Execute if intro is a Dictionary
            # This means options that jump to next scene
            for paragraph in scene[scene_section]:
                #print(scene[scene_section][paragraph])
                text = scene[scene_section][paragraph]['text'] + ' | ' + scene[scene_section][paragraph]['link']
                print(text)

        elif isinstance(scene[scene_section], list) == True:
            # Execute if intro is a List
            # Loop through intro and print the paragraphs
            # This means no options just text
            for paragraph in scene[scene_section]:
                print(paragraph)

storyProcessing()