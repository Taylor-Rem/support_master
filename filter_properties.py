from os_interact import OSInteract, JsonOperations

class FilterProperties:
    def __init__(self, report):
        os_interact = OSInteract()
        self.properties, self.units, self.residents = os_interact.retrieve_report_info(
            report
        )

    def current_report_items(self):
        current_report_items = []
        for i in range(len(self.property_names)):
            property = self.properties[i]
            resident = self.residents[i]
            unit = self.units[i]
            propunit = property + "_" + resident + "_" + str(unit)
            current_report_items.append(propunit)
        return current_report_items

    def filter_properties(self):
        set1 = set(self.current_report_items())
        set2 = set(self.json_interact.retrieve_json())
        unique_elements = (set1 - set2) | (set2 - set1)
        properties = []
        residents = []
        units = []
        for item in unique_elements:
            prop, res, unit = item.split("_")
            properties.append(prop)
            residents.append(res)
            units.append(unit)
        return properties, residents, units
