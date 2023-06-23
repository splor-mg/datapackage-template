from frictionless import Package

package = Package('datapackage.yaml')
package.dereference()

package.to_json('build/datapackage.json')
package.publish(f'sqlite:///build/{package.name}.db')
