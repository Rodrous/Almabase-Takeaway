from dataclasses import dataclass, field
import datetime
from typing import Optional, List, Dict
from thefuzz import fuzz
import asyncio


@dataclass
class Profile:
    first_name: str
    last_name: str
    date_of_birth: Optional[datetime.date]
    email_field: str
    class_year: Optional[int]


class Solution:
    @staticmethod
    async def find_duplicates(profiles: List[Profile], fields: List[str]) -> Dict | str:
        result_dict: Dict = {}
        total_score: int = 0
        common_attributes: Optional[List[str]] = []
        ignored_attributes: Optional[List[str]] = []
        for attributes in fields:
            if attributes == "class_year":
                if profiles[0].class_year and profiles[1].class_year:

                    if profiles[0].class_year == profiles[1].class_year and profiles[0].class_year == profiles[
                        1].class_year:
                        common_attributes.append(attributes)
                        total_score += 1
                    elif profiles[0].class_year == profiles[1].class_year and profiles[0].class_year != profiles[
                        1].class_year:
                        total_score -= 1
                else:
                    ignored_attributes.append("class_year")

            if attributes == "date_of_birth":
                if profiles[0].date_of_birth and profiles[1].date_of_birth:
                    if profiles[0].date_of_birth == profiles[1].date_of_birth and profiles[0].date_of_birth == profiles[
                        1].date_of_birth:
                        common_attributes.append(attributes)
                        total_score += 1
                    elif profiles[0].date_of_birth == profiles[1].date_of_birth and profiles[0].date_of_birth != \
                            profiles[
                                1].date_of_birth:
                        total_score -= 1
                else:
                    ignored_attributes.append("date_of_birth")

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
            if not ignored_attributes:
                ignored_attributes = None
            result_dict["Profiles"] = profiles
            result_dict["total_match_score"] = total_score
            result_dict["matching_attributes"] = common_attributes
            result_dict["non_matching_attributes"] = non_common_attributes
            result_dict["ignored_attributes"] = ignored_attributes
        else:
            return "Not Matching"

        return result_dict


async def main():
    profile_1 = Profile(
        email_field="knowkanhai@gmail.com",
        first_name="Kanhai",
        last_name="Shah",
        class_year=2012,
        date_of_birth=datetime.date(1990, 10, 11)
    )

    profile_2 = Profile(
        email_field="knowkanhai@gmail.com",
        first_name="Kanhail",
        last_name="Shah",
        class_year=2012,
        date_of_birth=datetime.date(1990, 10, 11)
    )

    profile_3 = Profile(
        email_field="knowkanhai@gmail.com",
        first_name="Kanhai",
        last_name="Shah",
        class_year=None,
        date_of_birth=None
    )

    profile_4 = Profile(
        email_field="knowkanhai@gmail.com",
        first_name="Kanhai1",
        last_name="Shah",
        class_year=2012,
        date_of_birth=datetime.date(1990, 10, 11)
    )
    solutionObj = Solution()
    results = await asyncio.gather(
        solutionObj.find_duplicates(profiles=[profile_1, profile_2], fields=["first_name", "last_name"]),
        solutionObj.find_duplicates(profiles=[profile_3,profile_4], fields=["first_name", "last_name","email_field", "class_year", "dete_of_birth"])


    )

    return results


if __name__ == "__main__":
    print(asyncio.run(main()))
