from dataclasses import dataclass, field
import datetime
from typing import Optional, List, Dict
from thefuzz import fuzz


@dataclass
class Profile:
    first_name: str
    last_name: str
    date_of_birth: Optional[datetime.date]
    email_field: str
    class_year: Optional[int]


class Solution:

    def find_duplicates(self, profiles: List[Profile], fields: List[str]) -> Dict:
        result_dict: Dict = {}
        total_score: int = 0
        common_attributes: List[str] = []

        for attributes in fields:
            if attributes == "class_year":
                if profiles[0].class_year == profiles[1].class_year and profiles[0].class_year == profiles[
                    1].class_year:
                    common_attributes.append(attributes)
                    total_score += 1
                elif profiles[0].class_year == profiles[1].class_year and profiles[0].class_year != profiles[
                    1].class_year:
                    total_score -= 1

            if attributes == "date_of_birth":
                if profiles[0].date_of_birth == profiles[1].date_of_birth and profiles[0].date_of_birth == profiles[
                    1].date_of_birth:
                    common_attributes.append(attributes)
                    total_score += 1
                elif profiles[0].date_of_birth == profiles[1].date_of_birth and profiles[0].date_of_birth != profiles[
                    1].date_of_birth:
                    total_score -= 1

        # If fields contains all ["first_name", "last_name", "email_field"]
        if all(attribute in fields for attribute in ["first_name", "last_name", "email_field"]):
            if fuzz.ratio(profiles[0].first_name, profiles[1].first_name) > 80 and fuzz.ratio(profiles[0].last_name,
                                                                                              profiles[
                                                                                                  1].last_name) > 80 and fuzz.ratio(
                    profiles[0].email_field, profiles[1].email_field) > 80:
                total_score += 1
                common_attributes.append("first_name")
                common_attributes.append("last_name")
                common_attributes.append("email_field")
        else:
            for attribute in fields:
                if attribute == "first_name":
                    if fuzz.ratio(profiles[0].first_name, profiles[1].first_name) > 80:
                        total_score += 0.33
                        common_attributes.append("first_name")
                elif attribute == "last_name":
                    if fuzz.ratio(profiles[0].last_name, profiles[1].last_name) > 80:
                        total_score += 0.33
                        common_attributes.append("last_name")
                elif attribute == "email_field":
                    if fuzz.ratio(profiles[0].email_field, profiles[1].email_field) > 80:
                        total_score += 0.33
                        common_attributes.append("email_field")

        total_score = round(total_score)

        # Building the result_dict
        if total_score >= 1:
            non_common_attributes = set(fields) ^ set(common_attributes) if set(fields) ^ set(
                common_attributes) else None
            elements_profile_1 = set(profiles[0].__dict__.keys())
            elements_profile_2 = set(profiles[1].__dict__.keys())
            total_attributes = elements_profile_1.union(elements_profile_2)

            result_dict["Profiles"] = profiles
            result_dict["total_match_score"] = total_score
            result_dict["matching_attributes"] = common_attributes.sort()
            result_dict["non_matching_attributes"] = non_common_attributes
            # result_dict["ignored_attributes"] = ignored_attributes

        return result_dict


if __name__ == "__main__":
    profile_1 = Profile(
        email_field="knowkanhai@gmail.com",
        first_name="Kanhai",
        last_name="Shah",
        class_year=None,
        date_of_birth=None
    )

    profile_2 = Profile(
        email_field="knowkanhai@gmail.com",
        first_name="Kanhail",
        last_name="Shah",
        class_year=2012,
        date_of_birth=datetime.date(1990, 10, 11)
    )

    Solution().find_duplicates([profile_1, profile_2], ["first_name", "last_name", "email_field"])
