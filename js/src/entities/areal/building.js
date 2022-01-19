import { useQueryGQL, Loading, LoadingError } from "../index";
import Card from "react-bootstrap/Card";
import { Link, useParams } from "react-router-dom";

import { root } from "../index";

const buildingRoot = root + '/areals/building';
export const BuildingSmall = (props) => {
    return <Link to={buildingRoot + `${props.id}`}>{props.name}{props.children}</Link>
}

export const BuildingMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                Budova
            </Card.Header>
            <Card.Body>
                {JSON.stringify(props)}
            </Card.Body>
        </Card>
    )
}

export const BuildingLarge = (props) => {
    return (
        <Card>
            <Card.Header>
                Budova
            </Card.Header>
            <Card.Body>
                {JSON.stringify(props)}
            </Card.Body>
        </Card>
    )
}

export const BuildingLargeStoryBook = (props) => {
    const extraProps = {
        'id' : 789,
        'name' : 'KŠ/9A',
        'rooms' : [
            {'id': 789, 'name': 'KŠ/9A/586'}
        ],
        'areal' : {'id' : 789, 'name': 'KŠ'},
        'user' : {'id' : 789, 'name': 'John', 'surname': 'Nowick'}
    }
    return <BuildingLarge {...extraProps} {...props} />
}

export const BuildingLargeQuery = (id) => 
    fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `
                query {
                    areal(id: ${id}) {
                      id
                      name
                      buildings {
                        id
                        name
                        rooms {
                          id
                          name
                        }
                      }
                    }
                  }
            `
        }),
    })

export const BuildingFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, ArealLargeQuery, (response) => response.data.areal, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <BuildingLargeStoryBook {...state} />
    } else {
        return <Loading>Budova {props.id}</Loading>
    }
}

export const _BuildingPage = (props) => {
    const { id } = useParams();

    return <BuildingFetching {...props} id={id} />;

}

export const BuildingPage = (props) => {
    const { id } = useParams();

    return <BuildingLargeStoryBook {...props} id={id} />;

}