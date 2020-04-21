
from matrx.agents.agent_types.human_agent import *
from custom_actions import *
from matrx.messages.message import Message


class CustomHumanAgentBrain(HumanAgentBrain):
    def __init__(self, state_memory_decay=1, fov_occlusion=False, max_carry_objects=3, grab_range=1, drop_range=1, door_range=1, remove_range=1):

        """
        Creates an Human Agent which is an agent that can be controlled by a human.
        """
        super().__init__()
        self.__state_memory_decay = state_memory_decay
        self.__fov_occlusion = fov_occlusion
        self.__max_carry_objects = max_carry_objects
        self.__remove_range = remove_range
        self.__grab_range = grab_range
        self.__drop_range = drop_range
        self.__door_range = door_range
        self.__remove_range = remove_range

    def decide_on_action(self, state, user_input):

        action_kwargs = {}

        # if no keys were pressed, do nothing
        if user_input is None or user_input == []:
            return None, {}

        # take the latest pressed key (for now), and fetch the action associated with that key
        pressed_keys = user_input[-1]
        action = self.key_action_map[pressed_keys]

        # if the user chose a grab action, choose an object within a grab_range of 1
        if action == GrabObject.__name__:
            # Assign it to the arguments list
            action_kwargs['grab_range'] = self.__grab_range  # Set grab range
            action_kwargs['max_objects'] = self.__max_carry_objects  # Set max amount of objects
            action_kwargs['object_id'] = None

            #obj_id = self.__select_random_obj_in_range(state, range_=self.__grab_range, property_to_check="is_movable")
            obj_id = self.__select_closest_obj_in_range(state, range_=self.__grab_range, property_to_check="is_movable")
            # Get agent id of Gravity God
            # object_ids = list(state.keys())
            # gravity_id = [obj_id for obj_id in object_ids if "GravityGod" in state[obj_id]['class']][0]

            # And send which location will then be empty to GravityGod
            #self.send_message(Message(content=state[obj_id]['location'], from_id=self.agent_id, to_id=None))
            action_kwargs['object_id'] = obj_id

        # If the user chose to drop an object in its inventory
        elif action == DropObject.__name__:
            # Assign it to the arguments list
            action_kwargs['drop_range'] = self.__drop_range  # Set drop range

        elif action == GrabLargeObject.__name__:
            # Assign it to the arguments list
            action_kwargs['grab_range'] = self.__grab_range  # Set grab range
            action_kwargs['max_objects'] = self.__max_carry_objects  # Set max amount of objects
            action_kwargs['object_id'] = None

            obj_id = self.__select_large_obj_in_range(state, range_=self.__grab_range, property_to_check="is_movable")
            action_kwargs['object_id'] = obj_id # This is a list now that contains the large object and its parts

        elif action == DropLargeObject.__name__:
            # Assign it to the arguments list
            action_kwargs['drop_range'] = self.__drop_range  # Set drop range

        # If the user chose to remove an object
        elif action == RemoveObject.__name__:
            # Assign it to the arguments list
            action_kwargs['remove_range'] = self.__remove_range  # Set drop range
            obj_id = self.__select_random_obj_in_range(state, range_=self.__remove_range, property_to_check="is_movable")
            action_kwargs['object_id'] = obj_id

        elif action == BreakObject.__name__:
            # Assign it to the arguments list
            action_kwargs['grab_range'] = self.__grab_range
            action_kwargs['object_id'] = None

            obj_id = self.__select_large_obj_in_range(state, range_=self.__grab_range, property_to_check="is_movable")
            action_kwargs['object_id'] = obj_id     # This is a list now that contains the large object and its parts

        # if the user chose to do an open or close door action, find a door to open/close within range
        elif action == OpenDoorAction.__name__ or action == CloseDoorAction.__name__:
            action_kwargs['door_range'] = self.__door_range
            action_kwargs['object_id'] = None

            # Get all doors from the perceived objects
            objects = list(state.keys())
            doors = [obj for obj in objects if 'is_open' in state[obj]]

            # get all doors within range
            doors_in_range = []
            for object_id in doors:
                # Select range as just enough to grab that object
                dist = int(np.ceil(np.linalg.norm(
                    np.array(state[object_id]['location']) - np.array(
                        state[self.agent_id]['location']))))
                if dist <= action_kwargs['door_range']:
                    doors_in_range.append(object_id)

            # choose a random door within range
            if len(doors_in_range) > 0:
                action_kwargs['object_id'] = self.rnd_gen.choice(doors_in_range)

        return action, action_kwargs

    def __select_random_obj_in_range(self, state, range_, property_to_check=None):
        # Get all perceived objects
        object_ids = list(state.keys())

        # Remove world from state
        object_ids.remove("World")

        # Remove self
        object_ids.remove(self.agent_id)

        # Remove all (human)agents
        object_ids = [obj_id for obj_id in object_ids if "AgentBrain" not in state[obj_id]['class_inheritance'] and
                      "AgentBody" not in state[obj_id]['class_inheritance']]

        # find objects in range
        object_in_range = []

        for object_id in object_ids:
            if "is_movable" not in state[object_id]:
                continue

            # Select range as just enough to grab that object
            dist = int(np.ceil(np.linalg.norm(np.array(state[object_id]['location'])
                                              - np.array(state[self.agent_id]['location']))))

            if dist <= range_:
                if property_to_check is not None:
                    if state[object_id][property_to_check]:
                        object_in_range.append(object_id)

        # Select an object if there are any in range
        if object_in_range:
            object_id = self.rnd_gen.choice(object_in_range)

        else:
            object_id = None

        return object_id

    def __select_closest_obj_in_range(self, state, range_, property_to_check=None):
        # Get all perceived objects
        object_ids = list(state.keys())

        # Remove world from state
        object_ids.remove("World")

        # Remove self
        object_ids.remove(self.agent_id)

        # Remove all (human)agents
        object_ids = [obj_id for obj_id in object_ids if "AgentBrain" not in state[obj_id]['class_inheritance'] and
                      "AgentBody" not in state[obj_id]['class_inheritance']]

        # find objects in range
        object_in_range = []
        distances = []

        for object_id in object_ids:
            if "is_movable" not in state[object_id]:
                continue

            # Select range as just enough to grab that object
            dist = int(np.ceil(np.linalg.norm(np.array(state[object_id]['location'])
                                              - np.array(state[self.agent_id]['location']))))

            if dist <= range_:
                if property_to_check is not None:
                    if state[object_id][property_to_check]:
                        object_in_range.append(object_id)
                        distances.append(dist)

        # Select an object if there are any in range
        if object_in_range:
            closest_dist = min(distances)
            closest_obj = object_in_range[distances.index(closest_dist)]
            object_id = closest_obj

        else:
            object_id = None

        return object_id

    def __select_large_obj_in_range(self, state, range_, property_to_check=None):
        # Get all perceived objects
        object_ids = list(state.keys())

        # Remove world from state
        object_ids.remove("World")

        # Remove self
        object_ids.remove(self.agent_id)

        # Remove all (human)agents
        object_ids = [obj_id for obj_id in object_ids if "AgentBrain" not in state[obj_id]['class_inheritance'] and
                      "AgentBody" not in state[obj_id]['class_inheritance']]

        # find objects in range
        object_in_range = []
        # find all parts of large object
        parts_obj_ids = []

        large_name = None

        for object_id in object_ids:
            if "is_movable" not in state[object_id]:
                continue

            # Only look at objects that are large
            if "large" not in state[object_id]:
                continue

            # Select range as just enough to grab that object
            dist = int(np.ceil(np.linalg.norm(np.array(state[object_id]['location'])
                                              - np.array(state[self.agent_id]['location']))))

            if dist <= range_:
                if property_to_check is not None:
                    if state[object_id][property_to_check]:
                        object_in_range.append(object_id)

        # Select closest large object
        if object_in_range:
            large_object_id = self.rnd_gen.choice(object_in_range)
            large_name = state[large_object_id]['name'] # And add to list of objects to pick up
            parts_obj_ids.append(large_object_id)

        # Now it's time to find the parts of this specific large object
        for object_id in object_ids:
            if "bound_to" not in state[object_id]:
                continue

            if state[object_id]['bound_to'] == large_name:
                parts_obj_ids.append(object_id)

        return parts_obj_ids


class GravityGod(AgentBrain):
    def __init__(self):
        super().__init__()

    def decide_on_action(self, state):
        action_kwargs = {}
        # List with all objects
        # Get all perceived objects
        object_ids = list(state.keys())
        # Remove world from state
        object_ids.remove("World")
        # Remove self
        object_ids.remove(self.agent_id)
        # Remove all (human)agents
        object_ids = [obj_id for obj_id in object_ids if "AgentBrain" not in state[obj_id]['class_inheritance'] and
                      "AgentBody" not in state[obj_id]['class_inheritance']]

        object_locs = []
        falling_objs = []
        skiplist = []

        # Create list with object locations
        for object_id in object_ids:
            object_loc = state[object_id]['location']
            object_locs.append(object_loc)

        # Check for each object whether the location below it is in the object locations list and pass all objects
        # with empty space beneath them to the Fall action
        for object_id in object_ids:
            object_loc = state[object_id]['location']
            object_loc_x = object_loc[0]
            object_loc_y = object_loc[1]
            if object_id in skiplist:
                continue
            if "large" or "bound_to" in state[object_id]:       # Seperate dealing with large objects
                large_obj = []      # List to contain all parts of large object
                if "large" in state[object_id]:
                    large_obj.append(object_id)     # Add to group for large object
                    skiplist.append(object_id)
                    large_name = state[object_id]['name']       # Identify name of large object from name
                    # Now find the parts!
                    for object_id_part in object_ids:
                        if "bound_to" not in state[object_id_part]:
                            continue
                        if state[object_id_part]['bound_to'] == large_name:
                            large_obj.append(object_id_part)
                            skiplist.append(object_id_part)
                elif "bound_to" in state[object_id]:
                    large_name = state[object_id]['bound_to']   # Identify name of large object from bound to
                    # Now find the parts and the large!
                    for object_id_part in object_ids:
                        if "bound_to" in state[object_id_part] and state[object_id_part]['bound_to'] == large_name:
                            large_obj.append(object_id_part)
                            skiplist.append(object_id_part)
                        elif "large" in state[object_id_part] and state[object_id_part]['name'] == large_name:
                            large_obj.append(object_id_part)
                            skiplist.append(object_id_part)
                if large_empty_check(large_obj, state, object_locs):
                    falling_objs.append(large_obj)
            if object_loc_y < 10:       # If the object is not already at ground level
                underneath_loc = (object_loc_x, object_loc_y + 1)
                if underneath_loc not in object_locs:       # If True, underneath_loc is empty!
                    falling_objs.append(object_id)

        # Activate Fall action if there are objects that should fall
        if falling_objs:
            action = Fall.__name__
            action_kwargs['object_list'] = falling_objs
        else:
            action = None

        return action, action_kwargs

def empty_notification(sender, object_id):
    return

def large_empty_check(large_obj, state, object_locs):
    y_locs = []
    for part in large_obj:
        object_loc = state[part]['location']
        object_loc_y = object_loc[1]
        y_locs.append(object_loc_y)

    lowest_y = max(y_locs, default=0)
    lowest_obj = [i for i in range(len(y_locs)) if y_locs[i] == lowest_y]     # List of objects with lowest y

    for obj_ind in lowest_obj:
        object_loc = state[large_obj[obj_ind]]['location']
        object_loc_x = object_loc[0]
        object_loc_y = object_loc[1]
        if object_loc_y < 10:
            underneath_loc = (object_loc_x, object_loc_y+1)
            if underneath_loc in object_locs:                   # If any location underneath is not empty, don't fall
                return False
        else:
            return False                        # If any object is already on the ground, don't fall

    return True